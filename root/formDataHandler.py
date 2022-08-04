import base64
import traceback
import uncertainpy.argumentation as arg
from uncertainpy.argumentation.graphing import graph
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


def return_invalid(reason):
    return [False, reason]


def isBase64(sb):
    # https://stackoverflow.com/a/45928164
    try:
        if isinstance(sb, str):
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def graph_from_ls(x):
    """Converts localstorage data to argumentation information"""
    try:
        # SET MODEL
        if (x['model_aside_dd'] == 'QuadraticEnergyModel'):
            model = arg.systems.QuadraticEnergyModel()
        else:
            return return_invalid('Invalid model error.')

        # SET APPROXIMATOR
        if (x['approx_aside_dd'] == 'RK4'):
            model.approximator = arg.approximators.RK4(model)
        else:
            return return_invalid('Invalid approximator error.')

        # SET BAG
        if (len(x['BAG']) > 0):
            # Convert BAG from b64 to string
            if (not isBase64(x['BAG'])):
                return return_invalid('Invalid BAG error.')

            bag = base64.b64decode(x['BAG']).decode()

            model.BAG = arg.BAG(bag)
        else:
            return return_invalid('Invalid BAG error.')

        if len(x['delta_aside_fl']) <= 0:
            return return_invalid('No Delta value provided')

        if len(x['epsilon_aside_fl']) <= 0:
            return return_invalid('No Epsilon value provided')

        try:
            float(x['epsilon_aside_fl'])
        except ValueError:
            return return_invalid('Invalid Epsilon error.')

        try:
            float(x['delta_aside_fl'])
        except ValueError:
            return return_invalid('Invalid Delta error.')

        DELTA = float(x['delta_aside_fl'])
        EPSILON = float(x['epsilon_aside_fl'])

        result = model.solve(delta=DELTA, epsilon=EPSILON, verbose=True, generate_plot=True)
        plot = graph(model, DELTA, EPSILON)

        plot_io_bytes = io.BytesIO()
        plot.savefig(plot_io_bytes, format='jpg')
        plot_io_bytes.seek(0)
        plotb64 = base64.b64encode(plot_io_bytes.read())

    except Exception as e:
        return return_invalid(str(e))

    return [True, plotb64.decode()]
