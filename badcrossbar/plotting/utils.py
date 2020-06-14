import numpy as np
import numpy.lib.recfunctions as nlr
from sigfig import round


def complete_path(ctx, rgb=(0, 0, 0), width=1):
    """Completes the current path.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    rgb : tuple of int
        Color of the path in RGB (normalized to 1).
    width : float
        Width of the path.
    """
    x, y = ctx.get_current_point()

    ctx.set_line_width(width)

    ctx.set_source_rgb(*rgb)

    ctx.stroke()
    ctx.move_to(x, y)


def complete_fill(ctx, rgb=(0, 0, 0)):
    """Completes the current fill.

    Parameters
    ----------
    ctx : cairo.Context
        Context.
    rgb : tuple of int
        Color of the fill in RGB (normalized to 1).
    """
    x, y = ctx.get_current_point()

    ctx.set_source_rgb(*rgb)

    ctx.fill()
    ctx.move_to(x, y)


def rgb_interpolation(array, low=0, high=1,
                      low_rgb=(213/255, 94/255, 0/255),
                      zero_rgb=(235/255, 235/255, 235/255),
                      high_rgb=(0/255, 114/255, 178/255)):
    """Linearly interpolates RGB colors for an array in a specified range.

    Parameters
    ----------
    array : ndarray
        Arrays of values.
    low : float
        Lower limit of the linear range.
    high : float
        Upper limit of the linear range.
    low_rgb : tuple of int
        Colour (in RGB) associated with the lower limit.
    zero_rgb : tuple of int
        Colour (in RGB) associated with value of zero.
    high_rgb : tuple of int
        Colour (in RGB) associated with the upper limit.
    Returns
    -------
    ndarray of tuple of int
        RGB values associated with each of the entries in the array.
    """
    rgb = []
    if low == 0:
        low = -1
    if high == 0:
        high = 1

    for low_x, zero_x, high_x in zip(low_rgb, zero_rgb, high_rgb):
        x = np.where(array > 0,
                     zero_x + (array - 0) * (high_x-zero_x)/(high-0),
                     low_x + (array - low) * (zero_x-low_x)/(0-low))

        rgb.append(x)

    rgb = np.array(rgb)
    rgb = np.moveaxis(rgb, 0, -1)
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def rgb_single_color(shape, color=(0, 0, 0)):
    """Return array with RGB values of a single color.

    Parameters
    ----------
    shape : tuple of int
        Shape of the array.
    color : tuple of int
        RGB (normalized to 1) of the color.

    Returns
    -------
    ndarray of tuple of int
        Array with RGB values.
    """
    rgb = np.ones((*shape, len(color))) * color
    rgb = nlr.unstructured_to_structured(rgb)
    if len(rgb.shape) == 0:
        rgb = rgb.reshape(1)
    return rgb


def arrays_range(*arrays):
    """Finds the color bar range from arbitrary number of arrays.

    Parameters
    ----------
    arrays : ndarray
        Arrays.

    Returns
    -------
    float
        Minimum and maximum values in the color bar.
    """
    low = np.inf
    high = -np.inf

    for array in arrays:
        if array is not None:
            minimum = np.min(array)
            if minimum < low:
                low = minimum

            maximum = np.max(array)
            if maximum > high:
                high = maximum

    if low == 0:
        low = 0
    if high == 0:
        high = 0

    if low != 0:
        low = round(float(low), sigfigs=2)
    if high != 0:
        high = round(float(high), sigfigs=2)

    if np.sign(low) != np.sign(high) and low != 0 and high != 0:
        maximum_absolute = np.max([np.abs(low), np.abs(high)])
        low = -maximum_absolute
        high = maximum_absolute
    return low, high


def arrays_shape(*arrays):
    """Returns the shape of the first array that is not None.

    Parameters
    ----------
    arrays : ndarray
        Arrays.

    Returns
    -------
    tuple of int
        Shape.
    """
    for array in arrays:
        if array is not None:
            shape = array.shape
            return shape
