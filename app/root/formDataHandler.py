import base64
import traceback

from ..uncertainpy.argumentation.BAG import BAGParseError
from ..uncertainpy import argumentation as arg
from ..uncertainpy.argumentation.graphing import graph
from ..uncertainpy.argumentation.Argument import Argument
import io
import networkx as nx
import matplotlib.pyplot as plt


def return_invalid(title, body):
    return [False, title, body]


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


def generate_model(x, return_vbo, draw_graph, draw_nodes) -> list:
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
                return return_invalid('Invalid Aggregation', 'The aggregation set in the aside panel is invalid. Try again with a different aggregation.')

            if x['inf_aside_dd'] == 'EulerBasedInfluence':
                model.influence = arg.influence.EulerBasedInfluence()

            elif x['inf_aside_dd'] == 'QuadraticMaximumInfluence':
                # Check if conservativeness is valid
                if len(x['inf_aside_fl']) <= 0:
                    return return_invalid('Invalid Conservativeness', 'The conservativeness value that you set is invalid. Try again with a different value. (Nothing to do with politics)')
                else:
                    try:
                        model.influence = arg.influence.QuadraticMaximumInfluence(conservativeness=float(x['inf_aside_fl']))
                    except ValueError:
                        return return_invalid('Invalid Conservativeness', 'The conservativeness value that you set is invalid. Try again with a different value. (Nothing to do with politics)')

            elif x['inf_aside_dd'] == 'LinearInfluence':
                # Check if conservativeness is valid
                if len(x['inf_aside_fl']) <= 0:
                    return return_invalid('Invalid Conservativeness', 'The conservativeness value that you set is invalid. Try again with a different value. (Nothing to do with politics)')
                else:
                    try:
                        model.influence = arg.influence.LinearInfluence(conservativeness=float(x['inf_aside_fl']))
                    except ValueError:
                        return return_invalid('Invalid Conservativeness', 'The conservativeness value that you set is invalid. Try again with a different value. (Nothing to do with politics)')
            else:
                return return_invalid('Invalid Influence', 'The influence set in the aside panel is invalid. Try again with a different influence.')
        else:
            return return_invalid('Invalid Model', 'The model you chose is invalid. Try again with a different model.')

        # SET APPROXIMATOR
        if (x['approx_aside_dd'] == 'RK4'):
            model.approximator = arg.approximators.RK4(model)
        else:
            return return_invalid('Invalid Approximator', 'The approximater you chose is invalid. Try again with a different approximator.')

        # SET BAG
        if (len(x['BAG']) > 0):
            # Convert BAG from b64 to string
            if (not isBase64(x['BAG'])):
                return return_invalid('Invalid BAG', 'Something went very wrong with the BAG input you provided.')

            bag = base64.b64decode(x['BAG']).decode()

            if x['BAG_LEGACY'] == 'legacy':
                is_legacy = True
            else:
                is_legacy = False

            model.BAG = arg.BAG(bag, legacy=is_legacy)

        else:
            return return_invalid('Invalid BAG', 'Something went wrong with the BAG input you provided. Perhaps you forgot to save?')

        if len(x['delta_aside_fl']) <= 0:
            return return_invalid('No Delta value provided', 'You must set a Delta value to proceed. (10e-2 is recommended)')

        if len(x['epsilon_aside_fl']) <= 0:
            return return_invalid('No Epsilon value provided', 'You must set an Epsilon value to proceed. (10e-4 is recommended)')

        try:
            float(x['epsilon_aside_fl'])
        except ValueError:
            return return_invalid('Invalid Epsilon value', 'The value you provided for Epsilon is invalid. Try again with a different value (10e-5 is recommended)')

        try:
            float(x['delta_aside_fl'])
        except ValueError:
            return return_invalid('Invalid Delta value', 'The value you provided for Delta is invalid. Try again with a different value (10e-2 is recommended)')

        DELTA = float(x['delta_aside_fl'])
        EPSILON = float(x['epsilon_aside_fl'])
        if (DELTA < 10e-4):
            return return_invalid('Invalid Delta value', 'The value for Delta cannot be less than 10e-4 for performance reasons. Try again with a greater value (10e-2 is recommended)')

        if (EPSILON < 10e-12):
            return return_invalid('Invalid Epsilon value', 'The value for Epsilon cannot be less than 10e-12 for performance reasons. Try again with a greater value (10e-4 is recommended)')
        r = model.solve(delta=DELTA, epsilon=EPSILON, verbose=return_vbo, generate_plot=draw_graph)

        if return_vbo:
            return [True, r]

        if draw_graph:
            plot = graph(model, DELTA, EPSILON, title="")
            plot_io_bytes = io.BytesIO()
            plot.savefig(plot_io_bytes, format='jpg')
            plot_io_bytes.seek(0)
            plotb64 = base64.b64encode(plot_io_bytes.read())
            return [True, plotb64.decode()]

        if draw_nodes:
            x = model.BAG.get_arguments()

            nodes = []
            node_widths = []
            # First we add all the arguments into the nodes array
            for a in x:
                nodes.append(a.name)
                node_widths.append(a.strength)

            edges = []
            edge_colors = []
            # Add attackers
            for a in x:
                for att in a.attackers:
                    edges.append((att.name, a.name, 1))
                    edge_colors.append('red')

            # Add supporters
            for a in x:
                for s in a.supporters:
                    edges.append((s.name, a.name, 1))
                    edge_colors.append('green')

            fig, ax = plt.subplots()

            G = nx.DiGraph()
            G.add_nodes_from(nodes)
            G.add_weighted_edges_from(edges)
            node_widths = list(map(lambda a: a*2000, node_widths))
            pos = nx.spring_layout(G)

            nx.draw(G, pos, with_labels=True, ax=ax, edge_color=edge_colors, node_size=node_widths, arrowsize=10, arrowstyle='simple')

            plot_io_bytes = io.BytesIO()
            plt.savefig(plot_io_bytes, format='jpg')
            plot_io_bytes.seek(0)
            plotb64 = base64.b64encode(plot_io_bytes.read())
            return [True, plotb64.decode()]

        return None
    
    except BAGParseError as e:
        return return_invalid('Invalid BAG', f'Something went wrong with the BAG input you provided.\nPerhaps you forgot to set the parsing mode to either Legacy (For newline BAG files) or Modern (For semicolon BAG files)?\n\n {e}')

    except OverflowError:
        return return_invalid('Overflow Error', 'Python has had an overflow error. You have probably set a value too large. (Probably Delta)')

    except Exception as e:
        print(traceback.format_exc())
        return return_invalid('Python Error', str(e))


def vbo_from_ls(x):
    """Converts localstorage data to argumentation information and returns verbose output"""
    vbo = generate_model(x=x, return_vbo=True, draw_graph=False, draw_nodes=False)
    if vbo is None:
        return return_invalid('Unknown error', 'I don\'t know how you managed this. Error code: 0x555')

    return vbo


def graph_from_ls(x):
    """Converts localstorage data to argumentation information and returns graphed data"""
    plotb64 = generate_model(x=x, return_vbo=False, draw_graph=True, draw_nodes=False)
    if plotb64 is None:
        return return_invalid('Unknown error', 'I don\'t know how you managed this. Error code: 0x556')

    return plotb64


def nodes_from_ls(x):
    """Converts localstorage data to argumentation information and returns node graph"""
    plotb64 = generate_model(x=x, return_vbo=False, draw_graph=False, draw_nodes=True)
    if plotb64 is None:
        return return_invalid('Unknown error', 'I don\'t know how you managed this. Error code: 0x556')

    return plotb64
