import base64
import traceback
import uncertainpy.argumentation as arg
from uncertainpy.argumentation.graphing import graph
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
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


def generate_model(x, return_vbo, draw_graph):
    """Creates model from localstorage data"""
    try:
        # SET MODEL
        if (x['model_aside_dd'] == 'QuadraticEnergyModel'):
            model = arg.systems.QuadraticEnergyModel()

        elif (x['model_aside_dd'] == 'ContinuousEulerBasedModel'):
            model = arg.systems.ContinuousEulerBasedModel()

        elif (x['model_aside_dd'] == 'ContinuousDFQuADModel'):
            model = arg.systems.ContinuousDFQuADModel()

        elif (x['model_aside_dd'] == 'ContinuousSquaredDFQuADModel'):
            model = arg.systems.ContinuousSquaredDFQuADModel()

        elif (x['model_aside_dd'] == 'SquaredEnergyModel'):
            model = arg.systems.SquaredEnergyModel()

        elif (x['model_aside_dd'] == 'ContinuousModularModel'):
            # It gets a bit crazy here
            model = arg.systems.ContinuousModularModel()
            if x['aggr_aside_dd'] == 'SumAggregation':
                model.aggregation = arg.aggregation.SumAggregation()
            elif x['aggr_aside_dd'] == 'ProductAggregation':
                model.aggregation = arg.aggregation.ProductAggregation()
            else:
                return return_invalid('Invalid aggregation error.')

            if x['inf_aside_dd'] == 'EulerBasedInfluence':
                model.influence = arg.influence.EulerBasedInfluence()

            elif x['inf_aside_dd'] == 'QuadraticMaximumInfluence':
                # Check if conservativeness is valid
                if len(x['inf_aside_fl']) <= 0:
                    return return_invalid('Invalid conservativeness error.')
                else:
                    try:
                        model.influence = arg.influence.QuadraticMaximumInfluence(conservativeness=float(x['inf_aside_fl']))
                    except ValueError:
                        return return_invalid('Invalid conservativeness error.')

            elif x['inf_aside_dd'] == 'LinearInfluence':
                # Check if conservativeness is valid
                if len(x['inf_aside_fl']) <= 0:
                    return return_invalid('Invalid conservativeness error.')
                else:
                    try:
                        model.influence = arg.influence.LinearInfluence(conservativeness=float(x['inf_aside_fl']))
                    except ValueError:
                        return return_invalid('Invalid conservativeness error.')

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

        r = model.solve(delta=DELTA, epsilon=EPSILON, verbose=return_vbo, generate_plot=draw_graph)

        if return_vbo:
            return r

        if draw_graph:
            plot = graph(model, DELTA, EPSILON, title="")
            plot_io_bytes = io.BytesIO()
            plot.savefig(plot_io_bytes, format='jpg')
            plot_io_bytes.seek(0)
            plotb64 = base64.b64encode(plot_io_bytes.read())
            return plotb64.decode()

        return None

    except Exception as e:
        print(traceback.format_exc())
        return return_invalid(str(e))


def vbo_from_ls(x):
    """Converts localstorage data to argumentation information and returns verbose output"""
    vbo = generate_model(x=x, return_vbo=True, draw_graph=False)
    if vbo is None:
        return return_invalid('Model error')
    return [True, vbo]


def graph_from_ls(x):
    """Converts localstorage data to argumentation information and returns graphed data"""
    plotb64 = generate_model(x=x, return_vbo=False, draw_graph=True)
    if plotb64 is None:
        return return_invalid('Model error')
    return [True, plotb64]
