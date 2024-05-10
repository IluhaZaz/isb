import logging
import argparse

from functions import find_number, luhn_algorithm, get_stats, draw_graph

from io_to_file import FileHandler


if __name__ == "__main__":

    logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{')

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-card','--get_card', help='Finds card by hash', action="store_true")
    group.add_argument('-luhn','--luhn_alg', help='Checks num with Luhn algorithm', action="store_true")
    group.add_argument('-graph','--draw_graph', help='Draws ghaph num_of_threads/seconds', action="store_true")

    parser.add_argument('-p', '--paths', type = str, help = 'Path to json file with paths')

    parser.add_argument('-ch', '--change_path', type = str, help = 'Change path to files')

    args = parser.parse_args()

    paths = FileHandler.read_json(args.paths, logger)

    constants = FileHandler.read_json(paths["constants"], logger)
    

    if args.change_path:
        temp = args.change_path.split(",")

        if temp[0] in paths.keys():
            paths[temp[0]] = temp[1]

    if args.get_card:
        find_number(constants["hash"], constants["last_4_nums"], constants["bins"], paths["card_number"], logger)
    
    elif args.luhn_alg:
        card_num: int = FileHandler.read_file(paths['card_number'], logger)
        print(f"Card number is {luhn_algorithm(card_num)}")
    
    elif args.draw_graph:
        data = get_stats(constants["hash"], constants["last_4_nums"], constants["bins"], logger, paths["times"])

        data = list(map(float, data))

        draw_graph(data, logger, paths["graph"])
    
    FileHandler.write_to_json(paths, args.paths, logger)
    #python main.py -card -p settings.json
    #python main.py -luhn -p settings.json
    #python main.py -graph -p settings.json
    #python main.py -ch graph,new_graph.png -p settings.json