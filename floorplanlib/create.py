import abc
import argparse
import os
import re
import subprocess
import sys


SILICON_SPECIFIC_HEAT_CAPACITY = 1.75e6
SILICON_THERMAL_RESISTIVITY = 0.01

TIM_SPECIFIC_HEAT_CAPACITY = 4e6
TIM_THERMAL_RESISTIVITY = 0.25

AIR_SPECIFIC_HEAT_CAPACITY = 2875000
AIR_THERMAL_RESISTIVITY = 0.13


HERE = os.path.dirname(os.path.abspath(__file__))


class Length(object):
    """
    distance stored in exact numbers in micrometers
    """
    def __init__(self, micrometers):
        self.micrometers = int(micrometers + 0.5)

    def __eq__(self, other):
        return self.micrometers == other.micrometers
    def __gt__(self, other):
        return self.micrometers > other.micrometers
    def __ge__(self, other):
        return self.micrometers >= other.micrometers

    def __mul__(self, v):
        return Length(v * self.micrometers)
    __rmul__ = __mul__

    def __add__(self, v):
        return Length(self.micrometers + v.micrometers)
    def __sub__(self, v):
        return Length(self.micrometers - v.micrometers)

    @property
    def meters(self):
        return self.micrometers / 1e6

    def __str__(self):
        return f'{self.meters:.6f}m'

    def __repr__(self):
        return f'Length({self.meters:.6f}m)'

    @classmethod
    def from_meters(self, v):
        return Length(v * 1e6)


def length(s):
    """ Parse length units. """
    units = {
        'm': 1e6,
        'dm': 1e5,
        'cm': 1e4,
        'mm': 1e3,
        'um': 1,
    }
    m = re.match(r'(?P<nb>\d+(\.\d+)?)(?P<unit>[a-z]+)', s)
    if not m:
        raise argparse.ArgumentTypeError(f'{s} is not a valid length. Valid examples are: 0.001m, 1mm, 980um')
    nb = float(m['nb'])
    if nb < 0:
        raise argparse.ArgumentTypeError('length cannot be negative')
    if m['unit'] not in units:
        units_str = ', '.join(units.keys())
        raise argparse.ArgumentTypeError(f'{m["unit"]} is not a valid unit of length. Valid units are: {units_str}')
    return Length(round(nb * units[m['unit']]))


def dimension_2d(s):
    pat = re.compile(r"(\d+)x(\d+)")
    m = pat.match(s)
    if not m:
        raise argparse.ArgumentTypeError('invalid format. Valid examples: 3x4, 8x8')
    return (int(m.group(1)), int(m.group(2)))


def dimension_3d(s):
    pat = re.compile(r"(\d+)x(\d+)x(\d+)")
    m = pat.match(s)
    if not m:
        raise argparse.ArgumentTypeError('invalid format. Valid examples: 4x4x2, 8x8x1')
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def dimension_2d_or_3d(s):
    try:
        return dimension_3d(s)
    except argparse.ArgumentTypeError:
        try:
            return dimension_2d(s)
        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError('invalid format. Valid examples: 4x4, 8x8x1')


def dimension_extend_to_3d(s):
    try:
        return dimension_3d(s)
    except argparse.ArgumentTypeError:
        try:
            a, b = dimension_2d(s)
            return a, b, 1
        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError('invalid format. Valid examples: 4x4, 8x8x1')


class FloorplanComponent(object):
    def __init__(self, name, width, height, left, bottom):
        self.name = name
        self.width = width
        self.height = height
        self.left = left
        self.bottom = bottom

    def format(self, endline=False):
        s = '{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}'.format(
            self.name, self.width.meters, self.height.meters, self.left.meters, self.bottom.meters)
        if endline:
            s += '\n'
        return s


class Floorplan(object):
    def __init__(self, components):
        self.components = components

    @property
    def width(self):
        return max(c.left + c.width for c in self.components) - self.left

    @property
    def height(self):
        return max(c.bottom + c.height for c in self.components) - self.bottom

    @property
    def left(self):
        return min(c.left for c in self.components)

    @property
    def bottom(self):
        return min(c.bottom for c in self.components)


def floorplan_file(s):
    components = []
    if not os.path.exists(s):
        raise argparse.ArgumentTypeError('file does not exist')
    with open(s) as f:
        for nb, line in enumerate(f):
            if line.strip().startswith('#'):
                continue
            else:
                pat = re.compile(r"([A-Za-z\-_0-9]+)\t(\d+\.\d+)\t(\d+\.\d+)\t(\d+\.\d+)\t(\d+\.\d+)")
                m = pat.match(line)
                if not m:
                    raise argparse.ArgumentTypeError(f'invalid floorplan file, parsing error on line {nb+1}')
                name = m.group(1)
                width = Length.from_meters(float(m.group(2)))
                height = Length.from_meters(float(m.group(3)))
                left = Length.from_meters(float(m.group(4)))
                bottom = Length.from_meters(float(m.group(5)))
                components.append(FloorplanComponent(name, width, height, left, bottom))
    return Floorplan(components)


class ThermalLayer(abc.ABC):
    """ base class for all thermal layers """
    def __init__(self, name):
        self.name = name

    def _get_floorplan_filename(self, directory):
        return os.path.join(directory, f'{self.name}.flp')

    def get_layer_configuration_string(self, directory, nb):
        return f'''\
# Layer "{self.name}"
{nb}
Y
{"Y" if self._has_power_consumption() else "N"}
{self._specific_heat_capacity()}
{self._thermal_resistivity()}
{self._thickness().meters}
{os.path.abspath(self._get_floorplan_filename(directory))}

'''

    @abc.abstractproperty
    def total_width(self):
        return self.elements[0] * self.element_width

    @abc.abstractproperty
    def total_height(self):
        return self.elements[1] * self.element_height

    @abc.abstractmethod
    def write_floorplan(self, directory):
        pass

    @abc.abstractmethod
    def _has_power_consumption(self):
        pass

    @abc.abstractmethod
    def _specific_heat_capacity(self):
        pass

    @abc.abstractmethod
    def _thermal_resistivity(self):
        pass

    @abc.abstractmethod
    def _thickness(self):
        pass


class SimpleLayer(ThermalLayer):
    """ base class for simple layers containing only one rectangular grid """
    def __init__(self, elements, element_width, element_height, thickness, name, nb_offset=0, pos_offset=None, subcomponent_template=None):
        super().__init__(name=name)
        self.elements = elements
        self.element_width = element_width
        self.element_height = element_height
        self.thickness = thickness
        self.nb_offset = nb_offset
        self.pos_offset = pos_offset if pos_offset is not None else (Length(0), Length(0))
        if subcomponent_template is not None:
            assert (subcomponent_template.left, subcomponent_template.bottom) == (Length(0), Length(0))
            assert (subcomponent_template.width, subcomponent_template.height) == (self.element_width, self.element_height)
        self.subcomponent_template = subcomponent_template

    @property
    def total_width(self):
        return self.elements[0] * self.element_width

    @property
    def total_height(self):
        return self.elements[1] * self.element_height

    def _thickness(self):
        return self.thickness

    def create_floorplan_elements(self):
        elements = []
        for y in range(self.elements[1]):
            for x in range(self.elements[0]):
                element_nb = self.nb_offset + y * self.elements[0] + x
                element_id = f'{self._get_element_identifier()}_{element_nb}'
                left = x * self.element_width + self.pos_offset[0]
                bottom = y * self.element_height + self.pos_offset[1]
                if self.subcomponent_template is None:
                    elements.append(
                        FloorplanComponent(
                            element_id,
                            self.element_width,
                            self.element_height,
                            left,
                            bottom))
                else:
                    for component in self.subcomponent_template.components:
                        subcomponent_id = f'{element_id}_{component.name}'
                        elements.append(
                            FloorplanComponent(
                                subcomponent_id,
                                component.width,
                                component.height,
                                left + component.left,
                                bottom + component.bottom))
        return ''.join(e.format(endline=True) for e in elements)

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\n')
            f.write(self.create_floorplan_elements())

    @abc.abstractmethod
    def _get_element_identifier(self):
        pass


class CoreLayer(SimpleLayer):
    """ a rectangular layer of cores """
    def _get_element_identifier(self):
        return 'C'

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY


class MemoryLayer(SimpleLayer):
    """ a rectangular layer of memory banks """
    def _get_element_identifier(self):
        return 'B'

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY


class MemoryControllerLayer(SimpleLayer):
    """ a rectangular layer of memory controllers """
    def _get_element_identifier(self):
        return 'LC'

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY


class TIMLayer(SimpleLayer):
    """ a rectangular layer of TIM """
    def _get_element_identifier(self):
        return 'TB'

    def _has_power_consumption(self):
        return False

    def _specific_heat_capacity(self):
        return TIM_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return TIM_THERMAL_RESISTIVITY


class InterposerLayer(SimpleLayer):
    """ a layer describing the interposer of 2.5D integration """
    def _get_element_identifier(self):
        return 'I'

    def _has_power_consumption(self):
        return False

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY


class CoreAndMemoryControllerLayer(ThermalLayer):
    """ first layer in 2.5D containing cores and memory controllers """
    def __init__(self, cores, core_width, core_height, banks, bank_width, bank_height, thickness, core_mem_distance, name, subcore_template):
        super().__init__(name=name)
        cores_width = cores[0] * core_width
        cores_height = cores[1] * core_width
        mem_width = banks[0] * bank_width
        mem_height = banks[1] * bank_height
        cores_offset = (
            Length(0),  # x
            Length(0) if cores_height > mem_height else 0.5 * (mem_height - cores_height)  # y
        )
        mem_offset = (
            cores_width + core_mem_distance,  # x
            Length(0) if mem_height > cores_height else 0.5 * (cores_height - mem_height)  # y
        )
        self.cores = CoreLayer(cores, core_width, core_height, thickness, name=None, pos_offset=cores_offset, subcomponent_template=subcore_template)
        self.memory_controllers = MemoryControllerLayer(banks, bank_width, bank_height, thickness, name=None, pos_offset=mem_offset)
        self.core_mem_distance = core_mem_distance
        self.thickness = thickness

    @property
    def total_width(self):
        return self.cores.total_width + self.core_mem_distance + self.memory_controllers.total_width

    @property
    def total_height(self):
        return max(self.cores.total_height, self.memory_controllers.total_height)

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')
            f.write(self.cores.create_floorplan_elements())
            f.write(self.memory_controllers.create_floorplan_elements())
            if self.cores.total_height >= self.memory_controllers.total_height:
                # add air blocks below and above memory
                h = 0.5 * (self.cores.total_height - self.memory_controllers.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.memory_controllers.total_width.meters, h.meters,
                    (self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.memory_controllers.total_width.meters, h.meters,
                    (self.cores.total_width + self.core_mem_distance).meters, (self.cores.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    self.cores.total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                # add air blocks below and above cores
                h = 0.5 * (self.memory_controllers.total_height - self.cores.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.cores.total_width.meters, h.meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.cores.total_width.meters, h.meters,
                    0, (self.memory_controllers.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.core_mem_distance.meters, self.memory_controllers.total_height.meters,
                    self.cores.total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY

    def _thickness(self):
        return self.thickness


class CoreAndMemoryControllerLayer_2_5D(ThermalLayer):
    """ first layer in 2.5D containing cores and memory controllers """
    def __init__(self, cores, core_width, core_height, drams, banks, bank_width, bank_height, thickness, cores_offset, mem_offset, nb_offset_core, nb_offset_mem, core_mem_distance, mem_mem_distance, name, subcore_template):
        super().__init__(name=name)
        cores_width = cores[0] * core_width
        cores_height = cores[1] * core_width
        mem_width = banks[0] * bank_width
        mem_height = banks[1] * bank_height
    
        self.cores = CoreLayer(cores, core_width, core_height, thickness, name=None, nb_offset=nb_offset_core, pos_offset=cores_offset, subcomponent_template=subcore_template)
        self.memory_controllers = []
        for i in range(drams):
            self.memory_controllers.append(MemoryControllerLayer(banks, bank_width, bank_height, thickness, name=None, nb_offset=nb_offset_mem[i], pos_offset=mem_offset[i]))
        self.core_mem_distance = core_mem_distance
        self.mem_mem_distance = mem_mem_distance
        self.thickness = thickness
        self.drams = drams

    @property
    def total_width(self):
        return self.cores.total_width + 2*self.core_mem_distance + 2*self.memory_controllers[0].total_width

    @property
    def total_height(self):
        return max(self.cores.total_height, 2*self.memory_controllers[0].total_height + self.mem_mem_distance)

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')
            f.write(self.cores.create_floorplan_elements())
            for i in range(self.drams):
                f.write(self.memory_controllers[i].create_floorplan_elements())

            if self.cores.total_height >= 2*self.memory_controllers[0].total_height + self.mem_mem_distance:
                # add air blocks below and above memory
                h = 0.5 * (self.cores.total_height - (2*self.memory_controllers[0].total_height + self.mem_mem_distance))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.memory_controllers[0].total_width.meters, h.meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.memory_controllers[1].total_width.meters, h.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory_controllers[0].total_width).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.memory_controllers[2].total_width.meters, h.meters,
                    0, (self.cores.total_height - h).meters ,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    self.memory_controllers[3].total_width.meters, h.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory_controllers[0].total_width).meters, (self.cores.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between memory and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X5',
                    self.memory_controllers[0].total_width.meters, self.mem_mem_distance.meters,
                    0, (h + self.memory_controllers[0].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X6',
                    self.memory_controllers[1].total_width.meters, self.mem_mem_distance.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory_controllers[0].total_width).meters, (h + self.memory_controllers[1].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    self.memory_controllers[0].total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    (self.memory_controllers[0].total_width + self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
        
            else:
                # add air blocks below and above memory
                h = 0.5 * ((2*self.memory_controllers[0].total_height + self.mem_mem_distance) - self.cores.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory_controllers[0].total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory_controllers[0].total_width + self.core_mem_distance).meters + self.cores.total_width.meters/2, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory_controllers[0].total_width + self.core_mem_distance).meters, (self.cores.total_height + h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory_controllers[0].total_width + self.core_mem_distance).meters + self.cores.total_width.meters/2, (self.cores.total_height + h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between memory and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X5',
                    self.memory_controllers[0].total_width.meters, self.mem_mem_distance.meters,
                    0, self.memory_controllers[0].total_height.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X6',
                    self.memory_controllers[1].total_width.meters, self.mem_mem_distance.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory_controllers[0].total_width).meters, self.memory_controllers[0].total_height.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    self.core_mem_distance.meters, (2*self.memory_controllers[0].total_height + self.mem_mem_distance).meters,
                    self.memory_controllers[0].total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    self.core_mem_distance.meters, (2*self.memory_controllers[0].total_height + self.mem_mem_distance).meters,
                    (self.memory_controllers[0].total_width + self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY

    def _thickness(self):
        return self.thickness





class CoreAndMemoryLayer(ThermalLayer):
    """ layer in 2.5D containing cores and memory banks """
    def __init__(self, cores, core_width, core_height, banks, bank_width, bank_height, thickness, core_mem_distance, nb_offset_core, nb_offset_mem, name, subcore_template):
        super().__init__(name=name)
        cores_width = cores[0] * core_width
        cores_height = cores[1] * core_width
        mem_width = banks[0] * bank_width
        mem_height = banks[1] * bank_height
        cores_offset = (
            Length(0),  # x
            Length(0) if cores_height > mem_height else 0.5 * (mem_height - cores_height)  # y
        )
        mem_offset = (
            cores_width + core_mem_distance,  # x
            Length(0) if mem_height > cores_height else 0.5 * (cores_height - mem_height)  # y
        )
        self.cores = CoreLayer(cores, core_width, core_height, thickness, name=None, nb_offset=nb_offset_core, pos_offset=cores_offset, subcomponent_template=subcore_template)
        self.memory = MemoryLayer(banks, bank_width, bank_height, thickness, name=None, nb_offset=nb_offset_mem, pos_offset=mem_offset)
        self.core_mem_distance = core_mem_distance
        self.thickness = thickness

    @property
    def total_width(self):
        return self.cores.total_width + self.core_mem_distance + self.memory.total_width

    @property
    def total_height(self):
        return max(self.cores.total_height, self.memory.total_height)

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')
            f.write(self.cores.create_floorplan_elements())
            f.write(self.memory.create_floorplan_elements())
            if self.cores.total_height >= self.memory.total_height:
                # add air blocks below and above memory
                h = 0.5 * (self.cores.total_height - self.memory.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.memory.total_width.meters, h.meters,
                    (self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.memory.total_width.meters, h.meters,
                    (self.cores.total_width + self.core_mem_distance).meters, (self.cores.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    self.cores.total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                # add air blocks below and above cores
                h = 0.5 * (self.memory.total_height - self.cores.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.cores.total_width.meters, h.meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.cores.total_width.meters, h.meters,
                    0, (self.memory.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.core_mem_distance.meters, self.memory.total_height.meters,
                    self.cores.total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY

    def _thickness(self):
        return self.thickness




class CoreAndMemoryLayer_2_5D(ThermalLayer):
    """ layer in 2.5D containing cores and memory banks """
    def __init__(self, cores, core_width, core_height, drams, banks, bank_width, bank_height, thickness, cores_offset, mem_offset, nb_offset_core, nb_offset_mem, core_mem_distance, mem_mem_distance, name, subcore_template):
        super().__init__(name=name)
        cores_width = cores[0] * core_width
        cores_height = cores[1] * core_width
        mem_width = banks[0] * bank_width
        mem_height = banks[1] * bank_height
    
        self.cores = CoreLayer(cores, core_width, core_height, thickness, name=None, nb_offset=nb_offset_core, pos_offset=cores_offset, subcomponent_template=subcore_template)
        self.memory = []
        for i in range(drams):
            self.memory.append(MemoryLayer(banks, bank_width, bank_height, thickness, name=None, nb_offset=nb_offset_mem[i], pos_offset=mem_offset[i]))
        self.core_mem_distance = core_mem_distance
        self.mem_mem_distance = mem_mem_distance
        self.thickness = thickness
        self.drams = drams

    @property
    def total_width(self):
        return self.cores.total_width + 2*self.core_mem_distance + 2*self.memory[0].total_width

    @property
    def total_height(self):
        return max(self.cores.total_height, 2*self.memory[0].total_height + self.mem_mem_distance)

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')
            f.write(self.cores.create_floorplan_elements())
            for i in range(self.drams):
                f.write(self.memory[i].create_floorplan_elements())

            if self.cores.total_height >= 2*self.memory[0].total_height + self.mem_mem_distance:
                # add air blocks below and above memory
                h = 0.5 * (self.cores.total_height - (2*self.memory[0].total_height + self.mem_mem_distance))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.memory[0].total_width.meters, h.meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.memory[1].total_width.meters, h.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory[0].total_width).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.memory[2].total_width.meters, h.meters,
                    0, (self.cores.total_height - h).meters ,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    self.memory[3].total_width.meters, h.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory[0].total_width).meters, (self.cores.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between memory and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X5',
                    self.memory[0].total_width.meters, self.mem_mem_distance.meters,
                    0, (h + self.memory[0].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X6',
                    self.memory[1].total_width.meters, self.mem_mem_distance.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory[0].total_width).meters, (h + self.memory[1].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    self.memory[0].total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    self.core_mem_distance.meters, self.cores.total_height.meters,
                    (self.memory[0].total_width + self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
        
            else:
                # add air blocks below and above memory
                h = 0.5 * ((2*self.memory[0].total_height + self.mem_mem_distance) - self.cores.total_height)
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory[0].total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory[0].total_width + self.core_mem_distance).meters + self.cores.total_width.meters/2, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory[0].total_width + self.core_mem_distance).meters, (self.cores.total_height + h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    self.cores.total_width.meters/2, h.meters,
                    (self.memory[0].total_width + self.core_mem_distance).meters + self.cores.total_width.meters/2, (self.cores.total_height + h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between memory and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X5',
                    self.memory[0].total_width.meters, self.mem_mem_distance.meters,
                    0, self.memory[0].total_height.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X6',
                    self.memory[1].total_width.meters, self.mem_mem_distance.meters,
                    (self.cores.total_width + 2*self.core_mem_distance + self.memory[0].total_width).meters, self.memory[0].total_height.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                # add air block between cores and memory
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    self.core_mem_distance.meters, (2*self.memory[0].total_height + self.mem_mem_distance).meters,
                    self.memory[0].total_width.meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    self.core_mem_distance.meters, (2*self.memory[0].total_height + self.mem_mem_distance).meters,
                    (self.memory[0].total_width + self.cores.total_width + self.core_mem_distance).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return SILICON_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return SILICON_THERMAL_RESISTIVITY

    def _thickness(self):
        return self.thickness



class PadWithAir(ThermalLayer):
    """ wrap a layer with air to match the given dimension """
    def __init__(self, total_width, total_height, thickness,name,force=None):
        super().__init__(name=name)
        self._total_width = total_width
        self._total_height = total_height
        self.thickness = thickness
        self.force = {'left': False, 'right': False, 'top': False, 'bottom': False} if force is None else force

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')

            # pad right
            f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                'X4',
                self.total_width.meters, self.total_height.meters,
                0, 0,
                AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return True

    def _specific_heat_capacity(self):
        return AIR_SPECIFIC_HEAT_CAPACITY

    def _thermal_resistivity(self):
        return AIR_THERMAL_RESISTIVITY

    def _thickness(self):
        return self.thickness


class PadWithAirLayer(ThermalLayer):
    """ wrap a layer with air to match the given dimension """
    def __init__(self, total_width, total_height, content, force=None):
        super().__init__(name=content.name)
        self._total_width = total_width
        self._total_height = total_height
        assert isinstance(content, SimpleLayer)
        self.content = content
        self.force = {'left': False, 'right': False, 'top': False, 'bottom': False} if force is None else force

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n')
            f.write(self.content.create_floorplan_elements())

            content_pos_offset = (Length(0), Length(0)) if self.content.pos_offset is None else self.content.pos_offset

            if content_pos_offset[1] > Length(0) or self.force.get('bottom'):
                # pad bottom
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.content.total_width.meters, content_pos_offset[1].meters,
                    content_pos_offset[0].meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            if content_pos_offset[1] + self.content.total_height < self.total_height or self.force.get('top'):
                # pad top
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.content.total_width.meters, (self.total_height - content_pos_offset[1] - self.content.total_height).meters,
                    content_pos_offset[0].meters, (content_pos_offset[1] + self.content.total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            if content_pos_offset[0] > Length(0) or self.force.get('left'):
                # pad left
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    content_pos_offset[0].meters, self.total_height.meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            if content_pos_offset[0] + self.content.total_width < self.total_width or self.force.get('right'):
                # pad right
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    (self.total_width - content_pos_offset[0] - self.content.total_width).meters, self.total_height.meters,
                    (content_pos_offset[0] + self.content.total_width).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return self.content._has_power_consumption()

    def _specific_heat_capacity(self):
        return self.content._specific_heat_capacity()

    def _thermal_resistivity(self):
        return self.content._thermal_resistivity()

    def _thickness(self):
        return self.content._thickness()



class PadWithAirLayer_2_5D(ThermalLayer):
    """ wrap a layer with air to match the given dimension """
    def __init__(self, drams, total_width, total_height, cores_width, cores_height, content, force=None):
        super().__init__(name=content[0].name)
        self._total_width = total_width
        self._total_height = total_height
        self.cores_width = cores_width
        self.cores_height = cores_height
        self.content = content
        self.force = {'left': False, 'right': False, 'top': False, 'bottom': False} if force is None else force
        self.drams = drams

    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    def write_floorplan(self, directory):
        with open(self._get_floorplan_filename(directory), 'w') as f:
            f.write('# Line Format: <unit-name>\\t<width>\\t<height>\\t<left-x>\\t<bottom-y>\\t[<specific-heat-capacity>\\t<thermal-resistivity>]\n') 
            for i in range(self.drams):
                f.write(self.content[i].create_floorplan_elements())

            h = 0.5 * (self.total_height - self.cores_height)
            # if self.content[0].pos_offset[1] > Length(0) or self.force.get('bottom'):
            if self.content[0].pos_offset[1] > Length(0):
                # pad bottom
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    self.content[0].total_width.meters, self.content[0].pos_offset[1].meters,
                    0, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X1',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, h.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            # if self.content[1].pos_offset[1] > Length(0) or self.force.get('bottom'):
            if self.content[1].pos_offset[1] > Length(0):
                # pad bottom
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    self.content[1].total_width.meters, self.content[1].pos_offset[1].meters,
                    self.content[1].pos_offset[0].meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X2',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, h.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters + (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            # if self.content[2].pos_offset[1] + self.content[2].total_height < self.total_height or self.force.get('top'):
            if self.content[2].pos_offset[1] + self.content[2].total_height < self.total_height:
                # pad top
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    self.content[2].total_width.meters, (self.total_height - self.content[2].pos_offset[1] - self.content[2].total_height).meters,
                    0, (self.content[2].pos_offset[1] + self.content[2].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X3',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, h.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters, (self.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            # if self.content[3].pos_offset[1] + self.content[2].total_height < self.total_height or self.force.get('top'):
            if self.content[3].pos_offset[1] + self.content[2].total_height < self.total_height:
                # pad top
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    self.content[3].total_width.meters, (self.total_height - self.content[3].pos_offset[1] - self.content[3].total_height).meters,
                    self.content[3].pos_offset[0].meters, (self.content[3].pos_offset[1] + self.content[3].total_height).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X4',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, h.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters + (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, (self.total_height - h).meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            # pad between memory
            f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                'X5',
                self.content[0].total_width.meters, (self.content[2].pos_offset[1] - self.content[0].pos_offset[1] - self.content[0].total_height).meters,
                0, (self.content[0].pos_offset[1] + self.content[0].total_height).meters,
                AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                'X6',
                self.content[1].total_width.meters, (self.content[3].pos_offset[1] - self.content[1].pos_offset[1] - self.content[1].total_height).meters,
                self.content[1].pos_offset[0].meters, (self.content[1].pos_offset[1] + self.content[1].total_height).meters,
                AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

            #pad centre
            if self.total_height == 2*self.content[0].total_height + self.content[2].pos_offset[1] - self.content[0].pos_offset[1] - self.content[0].total_height:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, (self.total_height - 2*h).meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters, h.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, (self.total_height - 2*h).meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters + (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, h.meters,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
            else:
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X7',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, self.total_height.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))
                f.write('{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\n'.format(
                    'X8',
                    (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, self.total_height.meters,
                    (self.content[0].pos_offset[0] + self.content[0].total_width).meters + (self.content[1].pos_offset[0] - self.content[0].pos_offset[0] - self.content[0].total_width).meters/2, 0,
                    AIR_SPECIFIC_HEAT_CAPACITY, AIR_THERMAL_RESISTIVITY))

    def _has_power_consumption(self):
        return self.content[0]._has_power_consumption()

    def _specific_heat_capacity(self):
        return self.content[0]._specific_heat_capacity()

    def _thermal_resistivity(self):
        return self.content[0]._thermal_resistivity()

    def _thickness(self):
        return self.content[0]._thickness()





class ThermalStack(object):
    def __init__(self, name, has_heatsink=True):
        self.name = name
        self.has_heatsink = has_heatsink
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def _write_lcf(self, directory):
        with open(os.path.join(directory, f'{self.name}.lcf'), 'w') as f:
            f.write('''\
#File Format:

#<Layer Number>
#<Lateral heat flow Y/N?>
#<Power Dissipation Y/N?>
#<Specific heat capacity in J/(m^3K)>
#<Resistivity in (m-K)/W>
#<Thickness in m>
#<floorplan file>

''')
            for nb, layer in enumerate(self.layers):
                f.write(layer.get_layer_configuration_string(directory, nb))

    def _write_hotspot_config(self, directory):
        with open(os.path.join(HERE, 'hotspot.config.tmpl'), 'r') as f:
            raw_content = f.read()
        chip_size = max(self.layers[0].total_width, self.layers[0].total_height).meters
        formatted_content = raw_content.format(
            s_solder=chip_size + 0.001,
            s_sub=chip_size + 0.02,
            s_spreader=chip_size + 0.02,
            s_sink=chip_size + 0.04,
            t_sink=0.0069 if self.has_heatsink else 0.00001,
        )
        with open(os.path.join(directory, f'{self.name}_hotspot.config'), 'w') as f:
            f.write(formatted_content)

    def _write_configuration_help(self, directory):
        pass  # TODO: implement

    def write_files(self, directory):
        for l in self.layers[1:]:
            assert l.total_width == self.layers[0].total_width
            assert l.total_height == self.layers[1].total_height

        if not os.path.exists(directory):
            os.makedirs(directory)

        for layer in self.layers:
            layer.write_floorplan(directory)
            # flp_to_pdf(layer._get_floorplan_filename(directory))  does not work due to fig2ps errors
        self._write_lcf(directory)
        self._write_hotspot_config(directory)
        self._write_configuration_help(directory)


def flp_to_pdf(filename):
    HOTSPOT_PATH = os.path.join(HERE, '..', 'hotspot_tool')

    assert filename[-4:] == '.flp'
    pdf_filename = filename[:-4] + '.pdf'

    tofig = subprocess.Popen([os.path.join(HOTSPOT_PATH, 'tofig.pl'), filename], stdout=subprocess.PIPE)
    fig2dev = subprocess.Popen(['fig2dev', '-L', 'ps'], stdin=tofig.stdout, stdout=subprocess.PIPE)  # crashes
    ps2pdf = subprocess.Popen(['ps2pdf', '-', pdf_filename], stdin=fig2dev.stdout)
    tofig.stdout.close()
    fig2dev.stdout.close()


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required named arguments')
    required.add_argument("--mode", help="chip architecture", choices=('DDR', '3Dmem', '2.5D', '3D'), required=True)
    cores = parser.add_argument_group('cores')
    cores.add_argument("--cores", help="number of cores", type=dimension_extend_to_3d, required=True)
    cores.add_argument("--corex", help="size of each core (in dimension x)", type=length, required=True)
    cores.add_argument("--corey", help="size of each core (in dimension y)", type=length, required=True)
    cores.add_argument("--core_thickness", help="thickness of the core silicon layer", type=length, required=False, default='50um')
    cores.add_argument("--subcore-template", help="template for sub-core components", type=floorplan_file, required=False)
    drams = parser.add_argument_group('drams')
    drams.add_argument("--drams",help="number of DRAMS", required=False, default=1)
    banks = parser.add_argument_group('memory banks')
    banks.add_argument("--banks", help="number of memory banks", type=dimension_2d_or_3d, required=True)
    banks.add_argument("--bankx", help="size of each memory bank (in dimension x)", type=length, required=True)
    banks.add_argument("--banky", help="size of each memory bank (in dimension y)", type=length, required=True)
    banks.add_argument("--bank_thickness", help="thickness of the bank silicon layer", type=length, required=False, default='50um')
    parser.add_argument("--core_mem_distance", help="only 2.5D: distance between cores and memory on interposer (default: 7mm)", type=length, required=False, default='7mm')
    parser.add_argument("--mem_mem_distance", help="only 2.5D: distance between memory and memory on interposer (default: 7mm)", type=length, required=False, default='3mm')
    parser.add_argument("--tim_thickness", help="thickness of the TIM", type=length, required=False, default='20um')
    parser.add_argument("--interposer_thickness", help="only 2.5D: thickness of the interposer", type=length, required=False, default='50um')
    parser.add_argument("--model_air", help="model air in 3Dmem", type=bool,required=False, default=False)
    required.add_argument("--out", help="directory in which the floorplan is stored", required=True)
    args = parser.parse_args()    

    cores_per_layer = args.cores[0] * args.cores[1]
    cores_2d = (args.cores[0], args.cores[1])

    if args.subcore_template is not None:
        if args.subcore_template.left != Length(0) or args.subcore_template.bottom != Length(0):
            parser.error('subcore-template must be positioned bottom left')
        if args.subcore_template.width != args.corex or args.subcore_template.height != args.corey:
            parser.error('subcore-template must be same size as a single core')

    if args.mode == 'DDR':
        if len(args.banks) != 2:
            parser.error('banks must be 2D in DDR mode. Example: --banks 4x4')

        core = ThermalStack('cores')
        for i in range(args.cores[2]):
            core.add_layer(CoreLayer(cores_2d, args.corex, args.corey, args.core_thickness, name=f'cores_{i+1}', nb_offset=i*cores_per_layer, subcomponent_template=args.subcore_template))
            core.add_layer(TIMLayer(cores_2d, args.corex, args.corey, args.tim_thickness, name='core_tim'))
        core.write_files(args.out)

        banks_2d = (args.banks[0], args.banks[1])
        mem = ThermalStack('mem', has_heatsink=False)
        mem.add_layer(MemoryLayer(args.banks, args.bankx, args.banky, args.bank_thickness, name='mem'))
        mem.add_layer(TIMLayer(banks_2d, args.bankx, args.banky, args.tim_thickness, name='mem_tim'))
        mem.write_files(args.out)

    elif args.mode == '3Dmem' and args.model_air == False:
        if len(args.banks) != 3:
            parser.error('banks must be 3D in 3Dmem mode. Example: --banks 4x4x2')

        banks_per_layer = args.banks[0] * args.banks[1]
        banks_2d = (args.banks[0], args.banks[1])

        core = ThermalStack('cores')
        for i in range(args.cores[2]):
            core.add_layer(CoreLayer(cores_2d, args.corex, args.corey, args.core_thickness, name=f'cores_{i+1}', nb_offset=i*cores_per_layer, subcomponent_template=args.subcore_template))
            core.add_layer(TIMLayer(cores_2d, args.corex, args.corey, args.tim_thickness, name='core_tim'))
        core.write_files(args.out)

        mem = ThermalStack('mem')
        mem.add_layer(MemoryControllerLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name='mem_ctrl'))
        tim = TIMLayer(banks_2d, args.bankx, args.banky, args.tim_thickness, name='mem_tim')
        for i in range(args.banks[2]):
            mem.add_layer(tim)
            mem.add_layer(MemoryLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name=f'mem_bank_{i+1}', nb_offset=i*banks_per_layer))
        mem.add_layer(tim)
        mem.write_files(args.out)

    elif args.mode == '3Dmem' and args.model_air == True:
        if len(args.banks) != 3:
            parser.error('banks must be 3D in 3Dmem mode. Example: --banks 4x4x2')

        cores_width = args.cores[0] * args.corex
        cores_height = args.cores[1] * args.corey
        mem_width = args.banks[0] * args.bankx
        mem_height = args.banks[1] * args.banky
        banks_per_layer = args.banks[0] * args.banks[1]
        banks_2d = (args.banks[0], args.banks[1])

        total_width = cores_width + args.core_mem_distance + mem_width
        total_height = max(cores_height, mem_height)

        # core_tim = TIMLayer(cores_2d, args.corex, args.corey, args.tim_thickness, name='core_tim')
        core_tim = TIMLayer((1, 1), total_width, total_height, args.tim_thickness, name='core_tim')
        mem_tim = TIMLayer((1, 1), total_width, total_height, args.tim_thickness, name='mem_tim')
        # core_interposer = InterposerLayer((1, 1), total_width, total_height, args.interposer_thickness, name='core_interposer')
        # mem_interposer = InterposerLayer((1, 1), total_width, total_height, args.interposer_thickness, name='mem_interposer')

        core_offset = (
            Length(0),  # x
            Length(0)  # y
        )

        mem_offset = (
            cores_width + args.core_mem_distance,  # x
            Length(0) if mem_height > cores_height else 0.5 * (cores_height - mem_height)  # y
        )

        core = ThermalStack('cores')
        # core.add_layer(core_interposer)
        # core.add_layer(core_tim)
        for i in range(args.cores[2]):
            core_layer = CoreLayer(cores_2d, args.corex, args.corey, args.core_thickness, name=f'cores_{i+1}', pos_offset=core_offset, nb_offset=i*cores_per_layer, subcomponent_template=args.subcore_template)
            core.add_layer(PadWithAirLayer(total_width, total_height, core_layer, force={'right': True}))
            # core.add_layer(CoreLayer(cores_2d, args.corex, args.corey, args.core_thickness, name=f'cores_{i+1}', nb_offset=i*cores_per_layer, subcomponent_template=args.subcore_template))
            core.add_layer(core_tim)

        for i in range(args.banks[2]+1-args.cores[2]):
            core.add_layer(PadWithAir(total_width, total_height, args.bank_thickness, name=f'air_{i+1}'))
            core.add_layer(core_tim)

        core.write_files(args.out)

        mem = ThermalStack('mem')
        # mem.add_layer(mem_interposer)
        # mem.add_layer(mem_tim)
        mem_ctrl = MemoryControllerLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name='mem_ctrl', pos_offset=mem_offset)
        mem.add_layer(PadWithAirLayer(total_width, total_height, mem_ctrl, force={'left': True, 'top': True, 'bottom': True}))
        
        for i in range(args.banks[2]):
            mem.add_layer(mem_tim)
            mem_banks =   MemoryLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name=f'mem_bank_{i+1}', pos_offset=mem_offset, nb_offset=i*banks_per_layer)
            mem.add_layer(PadWithAirLayer(total_width, total_height, mem_banks, force={'left': True, 'top': True, 'bottom': True}))
        mem.add_layer(mem_tim)
        mem.write_files(args.out)

    elif args.mode == '2.5D' and int(args.drams) == 1:
        if len(args.banks) != 3:
            parser.error('banks must be 3D in 2.5D mode. Example: --banks 4x4x2')

        # if args.cores[2] != 1:
        #     parser.error(f'2.5D currently only supports 1 core layer (requested {args.cores[2]})')

        if args.core_thickness != args.bank_thickness:
            parser.error(f'core and bank thickness must be the same in 2.5D (requested {args.core_thickness} and {args.bank_thickness})')

        cores_width = args.cores[0] * args.corex
        cores_height = args.cores[1] * args.corey
        mem_width = args.banks[0] * args.bankx
        mem_height = args.banks[1] * args.banky
        banks_per_layer = args.banks[0] * args.banks[1]
        banks_2d = (args.banks[0], args.banks[1])

        total_width = cores_width + args.core_mem_distance + mem_width
        total_height = max(cores_height, mem_height)

        stack = ThermalStack('stack')
        stack.add_layer(InterposerLayer((1, 1), total_width, total_height, args.interposer_thickness, name='interposer'))
        tim = TIMLayer((1, 1), total_width, total_height, args.tim_thickness, name='tim')
        stack.add_layer(tim)
        stack.add_layer(CoreAndMemoryControllerLayer(
            cores_2d, args.corex, args.corey,
            banks_2d, args.bankx, args.banky, args.core_thickness,
            args.core_mem_distance,
            name='core_and_mem_ctrl',
            subcore_template=args.subcore_template))
        mem_offset = (
            cores_width + args.core_mem_distance,  # x
            Length(0) if mem_height > cores_height else 0.5 * (cores_height - mem_height)  # y
        )


        for i in range(min(args.cores[2]-1,args.banks[2])):
            stack.add_layer(tim)
            stack.add_layer(CoreAndMemoryLayer(
                cores_2d, args.corex, args.corey,
                banks_2d, args.bankx, args.banky, args.core_thickness,
                args.core_mem_distance,
                (i+1)*cores_per_layer, i*banks_per_layer,
                name=f'core_and_mem_bank_{i+1}',
                subcore_template=args.subcore_template))


        for i in range(min(args.cores[2]-1,args.banks[2]),args.banks[2]):
            stack.add_layer(tim)
            mem_banks = MemoryLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name=f'mem_bank_{i+1}', pos_offset=mem_offset, nb_offset=i*banks_per_layer)
            stack.add_layer(PadWithAirLayer(total_width, total_height, mem_banks, force={'left': True, 'top': True, 'bottom': True}))
        stack.add_layer(tim)
        stack.write_files(args.out)





    elif args.mode == '2.5D':

        if len(args.banks) != 3:
            parser.error('banks must be 3D in 2.5D mode. Example: --banks 4x4x2')

        if args.core_thickness != args.bank_thickness:
            parser.error(f'core and bank thickness must be the same in 2.5D (requested {args.core_thickness} and {args.bank_thickness})')

        cores_width = args.cores[0] * args.corex
        cores_height = args.cores[1] * args.corey
        mem_width = args.banks[0] * args.bankx
        mem_height = args.banks[1] * args.banky
        num_drams = int(args.drams)
        banks_per_layer = args.banks[0] * args.banks[1] * num_drams
        banks_per_dram = args.banks[0] * args.banks[1] * args.banks[2]
        banks_per_dram_layer = args.banks[0] * args.banks[1]
        banks_2d = (args.banks[0], args.banks[1])
        curr_nb_offset_core = 0
        curr_nb_offset_mem = []
        for i in range(num_drams):
            curr_nb_offset_mem.append(i*banks_per_dram)

        cores_offset = (length('9.828mm'),length('2.576mm'))
        mem_offset = [(length('0.0mm'),length('0.0mm')),(length('24.332mm'),length('0.0mm')),(length('0.0mm'),length('9.828mm')),(length('24.332mm'),length('9.828mm'))]
        core_mem_distance = cores_offset[0] - mem_width
        mem_mem_distance = mem_offset[2][1] - mem_offset[0][1] - mem_height

        total_width = cores_width + 2*core_mem_distance + 2*mem_width
        total_height = max(cores_height, 2*mem_height + mem_mem_distance)

        stack = ThermalStack('stack')
        stack.add_layer(InterposerLayer((1, 1), total_width, total_height, args.interposer_thickness, name='interposer'))
        tim = TIMLayer((1, 1), total_width, total_height, args.tim_thickness, name='tim')
        stack.add_layer(tim)
        stack.add_layer(CoreAndMemoryControllerLayer_2_5D(
            cores_2d, args.corex, args.corey,
            num_drams,
            banks_2d, args.bankx, args.banky, args.core_thickness,
            cores_offset, mem_offset,
            curr_nb_offset_core, curr_nb_offset_mem,
            core_mem_distance, mem_mem_distance,
            name='core_and_mem_ctrl',
            subcore_template=args.subcore_template))

        # for i in range(num_drams):
        #     curr_nb_offset_mem[i] = i*banks_per_dram

        for i in range(min(args.cores[2]-1,args.banks[2])):
            curr_nb_offset_core = curr_nb_offset_core + cores_per_layer
            stack.add_layer(tim)
            stack.add_layer(CoreAndMemoryLayer_2_5D(
                cores_2d, args.corex, args.corey,
                num_drams,
                banks_2d, args.bankx, args.banky, args.core_thickness,
                cores_offset, mem_offset,
                curr_nb_offset_core, curr_nb_offset_mem,
                core_mem_distance, mem_mem_distance,
                name=f'core_and_mem_bank_{i+1}',
                subcore_template=args.subcore_template))
            for j in range(num_drams):
                curr_nb_offset_mem[j] = curr_nb_offset_mem[j] + banks_per_dram_layer


        for i in range(min(args.cores[2]-1,args.banks[2]),args.banks[2]):
            stack.add_layer(tim)
            mem_banks = []
            for j in range(num_drams):
                mem_banks.append(MemoryLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name=f'mem_bank_{i+1}', pos_offset=mem_offset[j], nb_offset=curr_nb_offset_mem[j]))
            stack.add_layer(PadWithAirLayer_2_5D(num_drams, total_width, total_height, cores_width, cores_height, mem_banks, force={'top': True, 'bottom': True}))
            for j in range(num_drams):
                curr_nb_offset_mem[j] = curr_nb_offset_mem[j] + banks_per_dram_layer
        stack.add_layer(tim)
        stack.write_files(args.out)




    elif args.mode == '3D':
        if len(args.banks) != 3:
            parser.error('banks must be 3D in 3D mode. Example: --banks 4x4x2')
        cores_width = args.cores[0] * args.corex
        cores_height = args.cores[1] * args.corey
        mem_width = args.banks[0] * args.bankx
        mem_height = args.banks[1] * args.banky
        if (cores_width, cores_height) != (mem_width, mem_height):
            parser.error('cores and banks must cover the same area in 3D mode')

        banks_per_layer = args.banks[0] * args.banks[1]
        banks_2d = (args.banks[0], args.banks[1])

        stack = ThermalStack('stack')
        tim = TIMLayer(banks_2d, args.bankx, args.banky, args.tim_thickness, name='tim')
        for i in range(args.banks[2]):
            stack.add_layer(MemoryLayer(banks_2d, args.bankx, args.banky, args.bank_thickness, name=f'mem_bank_{i+1}', nb_offset=i*banks_per_layer))
            stack.add_layer(tim)

        for i in range(args.cores[2]):
            stack.add_layer(CoreLayer(cores_2d, args.corex, args.corey, args.core_thickness, name=f'cores_{i+1}', nb_offset=i*cores_per_layer, subcomponent_template=args.subcore_template))
            stack.add_layer(tim)

        stack.write_files(args.out)
    else:
        raise Exception('unknown mode')

    with open(os.path.join(args.out, 'commandline.txt'), 'w') as f:
        f.write(f'''\
# command used to create these files:
{" ".join(sys.argv)}''')


if __name__ == '__main__':
    main()
