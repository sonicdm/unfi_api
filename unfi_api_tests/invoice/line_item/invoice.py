from unittest import TestCase
from unfi_api.invoice import get_invoice_html_tables, parse_table_with_labels_on_left, index_line_item_table
from unfi_api.invoice.line_item import LineItem
from devtools import debug
line_items_dict = {
    1: {'LN': '1', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/6 PACK', 'Pallet Name': '', 'UPC': '028833041106',
        'Product Code': '16323', 'Brand': '#ALVARADO', 'Product Desc': 'OG3 ALV SPR ON/POPPY BAG', 'Tax': '',
        'Whls. Cs. T': '22.27', 'Whls. Ea.': '3.7117', 'Reg SRP': '5.15', 'Weight': '8.60', 'Ext. Cube': '0.64',
        'Discount': '', 'Net - Case': '22.27', 'Net - Each': '3.7117', 'SRP': '5.15', 'Margin': '28',
        'Ext. Price': '22.27', 'Disc. Reas': ''},
    2: {'LN': '2', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/24 OZ', 'Pallet Name': '', 'UPC': '073472001011',
        'Product Code': '16804', 'Brand': '#FOOD/LIFE', 'Product Desc': 'OG2 FFL 7 GRN SP WHEAT', 'Tax': '',
        'Whls. Cs. T': '27.56', 'Whls. Ea.': '4.5933', 'Reg SRP': '6.39', 'Weight': '10.20', 'Ext. Cube': '0.72',
        'Discount': '15%', 'Net - Case': '23.4260', 'Net - Each': '3.9043', 'SRP': '6.39', 'Margin': '39',
        'Ext. Price': '23.43', 'Disc. Reas': 'S'},
    3: {'LN': '3', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '6/24 OZ', 'Pallet Name': '', 'UPC': '073472001417',
        'Product Code': '71942', 'Brand': '#FOOD/LIFE', 'Product Desc': 'OG2 FFL GEN 1:29 SPRTD', 'Tax': '',
        'Whls. Cs. T': '31.96', 'Whls. Ea.': '5.3267', 'Reg SRP': '7.39', 'Weight': '0.00', 'Ext. Cube': '0.00',
        'Discount': '', 'Net - Case': '31.96', 'Net - Each': '5.3267', 'SRP': '7.39', 'Margin': '28',
        'Ext. Price': '0.00', 'Disc. Reas': ''},
    4: {'LN': '4', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/17.4 OZ', 'Pallet Name': '', 'UPC': '867481000116',
        'Product Code': '69860', 'Brand': '#HAPPYCAMP', 'Product Desc': 'OG2 HCGF BRD BKWHT ML GF', 'Tax': '',
        'Whls. Cs. T': '40.27', 'Whls. Ea.': '6.7117', 'Reg SRP': '9.29', 'Weight': '6.80', 'Ext. Cube': '0.58',
        'Discount': '4.30', 'Net - Case': '35.97', 'Net - Each': '5.9950', 'SRP': '9.29', 'Margin': '35',
        'Ext. Price': '35.97', 'Disc. Reas': 'P'},
    5: {'LN': '5', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '12/11 OZ', 'Pallet Name': '', 'UPC': '834183001055',
        'Product Code': '70719', 'Brand': '@ALEXIA', 'Product Desc': 'ALEXIA GLDN ONIONS SSALT', 'Tax': '',
        'Whls. Cs. T': '43.73', 'Whls. Ea.': '3.6442', 'Reg SRP': '5.05', 'Weight': '0.00', 'Ext. Cube': '0.00',
        'Discount': '', 'Net - Case': '43.73', 'Net - Each': '3.6442', 'SRP': '5.05', 'Margin': '28',
        'Ext. Price': '0.00', 'Disc. Reas': ''},
    6: {'LN': '6', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/15 OZ', 'Pallet Name': '', 'UPC': '834183001093',
        'Product Code': '70720', 'Brand': '@ALEXIA', 'Product Desc': 'ALEXIA PARM/GARLIC REDS', 'Tax': '',
        'Whls. Cs. T': '38.55', 'Whls. Ea.': '3.2125', 'Reg SRP': '4.45', 'Weight': '12.15', 'Ext. Cube': '0.70',
        'Discount': '', 'Net - Case': '38.55', 'Net - Each': '3.2125', 'SRP': '4.45', 'Margin': '28',
        'Ext. Price': '38.55', 'Disc. Reas': ''},
    7: {'LN': '7', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/10.2 OZ', 'Pallet Name': '', 'UPC': '731789123450',
        'Product Code': '76344', 'Brand': '@AM FLTBRD', 'Product Desc': 'AFB VEGAN HARVEST PIZZA_', 'Tax': '',
        'Whls. Cs. T': '40.18', 'Whls. Ea.': '6.6967', 'Reg SRP': '9.29', 'Weight': '5.60', 'Ext. Cube': '0.68',
        'Discount': '', 'Net - Case': '40.18', 'Net - Each': '6.6967', 'SRP': '9.29', 'Margin': '28',
        'Ext. Price': '40.18', 'Disc. Reas': ''},
    8: {'LN': '8', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '12/5.5 OZ', 'Pallet Name': '', 'UPC': '042272009893',
        'Product Code': '25289', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS BN/QNOA BRTO GF', 'Tax': '',
        'Whls. Cs. T': '33.29', 'Whls. Ea.': '2.7742', 'Reg SRP': '3.85', 'Weight': '0.00', 'Ext. Cube': '0.00',
        'Discount': '', 'Net - Case': '33.29', 'Net - Each': '2.7742', 'SRP': '3.85', 'Margin': '28',
        'Ext. Price': '0.00', 'Disc. Reas': ''},
    9: {'LN': '9', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/14.5 OZ', 'Pallet Name': '', 'UPC': '042272001910',
        'Product Code': '73318', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS 3 CHEESE PIZZA', 'Tax': '',
        'Whls. Cs. T': '59.40', 'Whls. Ea.': '7.4250', 'Reg SRP': '10.29', 'Weight': '0.00', 'Ext. Cube': '0.00',
        'Discount': '', 'Net - Case': '59.40', 'Net - Each': '7.4250', 'SRP': '10.29', 'Margin': '28',
        'Ext. Price': '0.00', 'Disc. Reas': ''},
    10: {'LN': '10', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/12 OZ', 'Pallet Name': '', 'UPC': '042272001002',
         'Product Code': '77276', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS RICE CRST PIZZA', 'Tax': '',
         'Whls. Cs. T': '63.33', 'Whls. Ea.': '7.9163', 'Reg SRP': '10.99', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '63.33', 'Net - Each': '7.9163', 'SRP': '10.99', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    11: {'LN': '11', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/13 OZ', 'Pallet Name': '', 'UPC': '042272001095',
         'Product Code': '77292', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS MSHRM/OLV PZZA', 'Tax': '',
         'Whls. Cs. T': '59.40', 'Whls. Ea.': '7.4250', 'Reg SRP': '10.29', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '59.40', 'Net - Each': '7.4250', 'SRP': '10.29', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    12: {'LN': '12', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/12 OZ', 'Pallet Name': '', 'UPC': '042272001033',
         'Product Code': '77306', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS RSTD VEGETABLE', 'Tax': '',
         'Whls. Cs. T': '59.40', 'Whls. Ea.': '7.4250', 'Reg SRP': '10.29', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '59.40', 'Net - Each': '7.4250', 'SRP': '10.29', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    13: {'LN': '13', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/13.5 OZ', 'Pallet Name': '', 'UPC': '042272001040',
         'Product Code': '77321', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS PESTO PZZA/TOM/', 'Tax': '',
         'Whls. Cs. T': '59.40', 'Whls. Ea.': '7.4250', 'Reg SRP': '10.29', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '59.40', 'Net - Each': '7.4250', 'SRP': '10.29', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    14: {'LN': '14', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/9.5 OZ', 'Pallet Name': '', 'UPC': '042272008117',
         'Product Code': '79554', 'Brand': '@AMYS', 'Product Desc': 'OG3 AMYS BROC CHED BOWL', 'Tax': '',
         'Whls. Cs. T': '54.28', 'Whls. Ea.': '4.5233', 'Reg SRP': '6.29', 'Weight': '10.20', 'Ext. Cube': '0.74',
         'Discount': '', 'Net - Case': '54.28', 'Net - Each': '4.5233', 'SRP': '6.29', 'Margin': '28',
         'Ext. Price': '54.28', 'Disc. Reas': ''},
    15: {'LN': '15', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/8 OZ', 'Pallet Name': '', 'UPC': '025317005500',
         'Product Code': '71044', 'Brand': '@APPLEGATE', 'Product Desc': 'OG2 AF CHICKEN STRIPS', 'Tax': '',
         'Whls. Cs. T': '83.40', 'Whls. Ea.': '6.95', 'Reg SRP': '9.65', 'Weight': '6.00', 'Ext. Cube': '0.71',
         'Discount': '', 'Net - Case': '83.40', 'Net - Each': '6.95', 'SRP': '9.65', 'Margin': '28',
         'Ext. Price': '83.40', 'Disc. Reas': ''},
    16: {'LN': '16', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '12/7 OZ', 'Pallet Name': '', 'UPC': '025317006965',
         'Product Code': '71383', 'Brand': '@APPLEGATE', 'Product Desc': 'AF CHKN MPL BRKFST SAUS', 'Tax': '',
         'Whls. Cs. T': '48.69', 'Whls. Ea.': '4.0575', 'Reg SRP': '5.65', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '48.69', 'Net - Each': '4.0575', 'SRP': '5.65', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    17: {'LN': '17', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '12/7 OZ', 'Pallet Name': '', 'UPC': '025317894005',
         'Product Code': '73501', 'Brand': '@APPLEGATE', 'Product Desc': 'AF BRKF SSG CHKN HERB', 'Tax': '',
         'Whls. Cs. T': '48.69', 'Whls. Ea.': '4.0575', 'Reg SRP': '5.65', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '48.69', 'Net - Each': '4.0575', 'SRP': '5.65', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    18: {'LN': '18', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/14 OZ', 'Pallet Name': '', 'UPC': '852629004750',
         'Product Code': '15119', 'Brand': '@BEYOND', 'Product Desc': 'B.M SAUSAGE HOT ITALIAN', 'Tax': '',
         'Whls. Cs. T': '60.65', 'Whls. Ea.': '7.5813', 'Reg SRP': '10.55', 'Weight': '7.00', 'Ext. Cube': '0.51',
         'Discount': '', 'Net - Case': '60.65', 'Net - Each': '7.5813', 'SRP': '10.55', 'Margin': '28',
         'Ext. Price': '60.65', 'Disc. Reas': ''},
    19: {'LN': '19', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/24 OZ', 'Pallet Name': '', 'UPC': '867624000201',
         'Product Code': '34421', 'Brand': '@BONAFIDE', 'Product Desc': 'OG2 BONA CHKN BONE BROTH', 'Tax': '',
         'Whls. Cs. T': '42.72', 'Whls. Ea.': '7.12', 'Reg SRP': '9.89', 'Weight': '10.00', 'Ext. Cube': '0.42',
         'Discount': '', 'Net - Case': '42.72', 'Net - Each': '7.12', 'SRP': '9.89', 'Margin': '28',
         'Ext. Price': '42.72', 'Disc. Reas': ''},
    20: {'LN': '20', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '12/16 OZ', 'Pallet Name': '', 'UPC': '021908501413',
         'Product Code': '74082', 'Brand': '@CASCADIAN', 'Product Desc': 'OG2 CASC MIXED VEGETABLE', 'Tax': '',
         'Whls. Cs. T': '31.81', 'Whls. Ea.': '2.6508', 'Reg SRP': '3.69', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '31.81', 'Net - Each': '2.6508', 'SRP': '3.69', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    21: {'LN': '21', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '8/14 OZ', 'Pallet Name': '', 'UPC': '799512012105',
         'Product Code': '76056', 'Brand': '@CIAO BELL', 'Product Desc': 'CIAO SIC BLD ORNG SRBTTO', 'Tax': '',
         'Whls. Cs. T': '34.26', 'Whls. Ea.': '4.2825', 'Reg SRP': '5.95', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '3.66', 'Net - Case': '30.60', 'Net - Each': '3.8250', 'SRP': '5.95', 'Margin': '36',
         'Ext. Price': '0.00', 'Disc. Reas': 'P'},
    22: {'LN': '22', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/3/3 OZ', 'Pallet Name': '', 'UPC': '896767001837',
         'Product Code': '27563', 'Brand': '@COCOBLISS', 'Product Desc': 'OG2 COBL CNUT ALM CHOC', 'Tax': '',
         'Whls. Cs. T': '61.66', 'Whls. Ea.': '5.1383', 'Reg SRP': '7.15', 'Weight': '8.26', 'Ext. Cube': '0.63',
         'Discount': '20%', 'Net - Case': '49.3280', 'Net - Each': '4.1107', 'SRP': '7.15', 'Margin': '43',
         'Ext. Price': '49.33', 'Disc. Reas': 'S'},
    23: {'LN': '23', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/PT', 'Pallet Name': '', 'UPC': '896767001011',
         'Product Code': '72221', 'Brand': '@COCOBLISS', 'Product Desc': 'OG2 COBL DARK CHOCOLATE', 'Tax': '',
         'Whls. Cs. T': '43.13', 'Whls. Ea.': '5.3913', 'Reg SRP': '7.49', 'Weight': '7.36', 'Ext. Cube': '0.25',
         'Discount': '20%', 'Net - Case': '34.5040', 'Net - Each': '4.3130', 'SRP': '7.49', 'Margin': '42',
         'Ext. Price': '34.50', 'Disc. Reas': 'S'},
    24: {'LN': '24', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/PT', 'Pallet Name': '', 'UPC': '896767001028',
         'Product Code': '72222', 'Brand': '@COCOBLISS', 'Product Desc': 'OG2 COBL MADA VAN BEAN', 'Tax': '',
         'Whls. Cs. T': '43.13', 'Whls. Ea.': '5.3913', 'Reg SRP': '7.49', 'Weight': '7.12', 'Ext. Cube': '0.24',
         'Discount': '20%', 'Net - Case': '34.5040', 'Net - Each': '4.3130', 'SRP': '7.49', 'Margin': '42',
         'Ext. Price': '34.50', 'Disc. Reas': 'S'},
    25: {'LN': '25', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/PT', 'Pallet Name': '', 'UPC': '896767001219',
         'Product Code': '72445', 'Brand': '@COCOBLISS', 'Product Desc': 'OG2 COBL CHOCOLATE PBTR', 'Tax': '',
         'Whls. Cs. T': '43.13', 'Whls. Ea.': '5.3913', 'Reg SRP': '7.49', 'Weight': '7.12', 'Ext. Cube': '0.22',
         'Discount': '20%', 'Net - Case': '34.5040', 'Net - Each': '4.3130', 'SRP': '7.49', 'Margin': '42',
         'Ext. Price': '34.50', 'Disc. Reas': 'S'},
    26: {'LN': '26', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/8.5 OZ', 'Pallet Name': '', 'UPC': '011433119702',
         'Product Code': '77500', 'Brand': '@DEEP', 'Product Desc': 'DEEP SPIN/PANR NAAN PZA', 'Tax': '',
         'Whls. Cs. T': '28.50', 'Whls. Ea.': '2.3750', 'Reg SRP': '3.29', 'Weight': '9.00', 'Ext. Cube': '0.68',
         'Discount': '', 'Net - Case': '28.50', 'Net - Each': '2.3750', 'SRP': '3.29', 'Margin': '28',
         'Ext. Price': '28.50', 'Disc. Reas': ''},
    27: {'LN': '27', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'DESCR',
         'Brand': '', 'Product Desc': 'Replaces PN 06959', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '', 'Reg SRP': '',
         'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    28: {'LN': '28', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/4/2.5Z', 'Pallet Name': '', 'UPC': '037295003584',
         'Product Code': '71762', 'Brand': '@DUTCHGIRL', 'Product Desc': 'FRTSTIX CRMY MANGO BAR', 'Tax': '',
         'Whls. Cs. T': '39.74', 'Whls. Ea.': '3.3117', 'Reg SRP': '4.59', 'Weight': '8.30', 'Ext. Cube': '0.53',
         'Discount': '', 'Net - Case': '39.74', 'Net - Each': '3.3117', 'SRP': '4.59', 'Margin': '28',
         'Ext. Price': '39.74', 'Disc. Reas': ''},
    29: {'LN': '29', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/4/2.5Z', 'Pallet Name': '', 'UPC': '037295003669',
         'Product Code': '76126', 'Brand': '@DUTCHGIRL', 'Product Desc': 'OG2 FRTSTIX STRAWBRY FB', 'Tax': '',
         'Whls. Cs. T': '44.87', 'Whls. Ea.': '3.7392', 'Reg SRP': '5.19', 'Weight': '9.60', 'Ext. Cube': '0.54',
         'Discount': '', 'Net - Case': '44.87', 'Net - Each': '3.7392', 'SRP': '5.19', 'Margin': '28',
         'Ext. Price': '44.87', 'Disc. Reas': ''},
    30: {'LN': '30', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/1 PINT', 'Pallet Name': '', 'UPC': '852109331178',
         'Product Code': '49369', 'Brand': '@ENLITE', 'Product Desc': 'ENLITE KETO CHOC PBTR', 'Tax': '',
         'Whls. Cs. T': '39.09', 'Whls. Ea.': '4.8863', 'Reg SRP': '6.79', 'Weight': '6.30', 'Ext. Cube': '0.27',
         'Discount': '', 'Net - Case': '39.09', 'Net - Each': '4.8863', 'SRP': '6.79', 'Margin': '28',
         'Ext. Price': '39.09', 'Disc. Reas': ''},
    31: {'LN': '31', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/16 OZ', 'Pallet Name': '', 'UPC': '785002324131',
         'Product Code': '77098', 'Brand': '@FILLO', 'Product Desc': 'OG2 FILLO DOUGH', 'Tax': '',
         'Whls. Cs. T': '55.71', 'Whls. Ea.': '4.6425', 'Reg SRP': '6.45', 'Weight': '13.65', 'Ext. Cube': '0.50',
         'Discount': '', 'Net - Case': '55.71', 'Net - Each': '4.6425', 'SRP': '6.45', 'Margin': '28',
         'Ext. Price': '55.71', 'Disc. Reas': ''},
    32: {'LN': '32', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/6.4 OZ', 'Pallet Name': '', 'UPC': '854262003008',
         'Product Code': '77217', 'Brand': '@HILARYS', 'Product Desc': 'HILARYS BEST VEGI BURGER', 'Tax': '',
         'Whls. Cs. T': '34.68', 'Whls. Ea.': '2.89', 'Reg SRP': '3.99', 'Weight': '5.00', 'Ext. Cube': '0.36',
         'Discount': '', 'Net - Case': '34.68', 'Net - Each': '2.89', 'SRP': '3.99', 'Margin': '28',
         'Ext. Price': '34.68', 'Disc. Reas': ''},
    33: {'LN': '33', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/PINT', 'Pallet Name': '', 'UPC': '854758001044',
         'Product Code': '71018', 'Brand': '@NADAMOO', 'Product Desc': 'OG3 NADA MAPLE PCN ICRM', 'Tax': '',
         'Whls. Cs. T': '40.25', 'Whls. Ea.': '5.0313', 'Reg SRP': '6.99', 'Weight': '5.87', 'Ext. Cube': '0.27',
         'Discount': '20%', 'Net - Case': '32.20', 'Net - Each': '4.0250', 'SRP': '6.99', 'Margin': '42',
         'Ext. Price': '32.20', 'Disc. Reas': 'S'},
    34: {'LN': '34', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '6/8 OZ', 'Pallet Name': '', 'UPC': '785030116920',
         'Product Code': '70641', 'Brand': '@RISING MN', 'Product Desc': 'OG2 RMO WLD MUSH RAVIOLI', 'Tax': '',
         'Whls. Cs. T': '25.91', 'Whls. Ea.': '4.3183', 'Reg SRP': '5.99', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '25.91', 'Net - Each': '4.3183', 'SRP': '5.99', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    35: {'LN': '35', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '6/8 OZ', 'Pallet Name': '', 'UPC': '785030555552',
         'Product Code': '70644', 'Brand': '@RISING MN', 'Product Desc': 'OG2 RMO CLSC PSTO RAVOLI', 'Tax': '',
         'Whls. Cs. T': '25.91', 'Whls. Ea.': '4.3183', 'Reg SRP': '5.99', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '25.91', 'Net - Each': '4.3183', 'SRP': '5.99', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    36: {'LN': '36', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '6/8 OZ', 'Pallet Name': '', 'UPC': '785030000113',
         'Product Code': '70650', 'Brand': '@RISING MN', 'Product Desc': 'OG2 RMO VEGN RST VEG RAV', 'Tax': '',
         'Whls. Cs. T': '25.91', 'Whls. Ea.': '4.3183', 'Reg SRP': '5.99', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '25.91', 'Net - Each': '4.3183', 'SRP': '5.99', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    37: {'LN': '37', 'Ord': '1', 'Shp': '0', 'Eaches - Pack': '6/8 OZ', 'Pallet Name': '', 'UPC': '785030555613',
         'Product Code': '70972', 'Brand': '@RISING MN', 'Product Desc': 'OG2 RMO SPIN CHEESE RAV', 'Tax': '',
         'Whls. Cs. T': '25.91', 'Whls. Ea.': '4.3183', 'Reg SRP': '5.99', 'Weight': '0.00', 'Ext. Cube': '0.00',
         'Discount': '', 'Net - Case': '25.91', 'Net - Each': '4.3183', 'SRP': '5.99', 'Margin': '28',
         'Ext. Price': '0.00', 'Disc. Reas': ''},
    38: {'LN': '38', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '10/5 OZ', 'Pallet Name': '', 'UPC': '856014001027',
         'Product Code': '76880', 'Brand': '@RUBYJEWEL', 'Product Desc': 'RUBY DK CHOC MINT CKY', 'Tax': '',
         'Whls. Cs. T': '31.89', 'Whls. Ea.': '3.1890', 'Reg SRP': '4.45', 'Weight': '3.75', 'Ext. Cube': '0.30',
         'Discount': '20%', 'Net - Case': '25.5120', 'Net - Each': '2.5512', 'SRP': '4.45', 'Margin': '43',
         'Ext. Price': '25.51', 'Disc. Reas': 'S'},
    39: {'LN': '39', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/5.25 OZ', 'Pallet Name': '', 'UPC': '860000298438',
         'Product Code': '54788', 'Brand': '@SAVORTOTH', 'Product Desc': 'OG2 STP PALEO PZZA CRUST', 'Tax': '',
         'Whls. Cs. T': '31.23', 'Whls. Ea.': '5.2050', 'Reg SRP': '7.25', 'Weight': '3.60', 'Ext. Cube': '0.24',
         'Discount': '3.37', 'Net - Case': '27.86', 'Net - Each': '4.6433', 'SRP': '7.25', 'Margin': '36',
         'Ext. Price': '27.86', 'Disc. Reas': 'P'},
    40: {'LN': '40', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8 PINT', 'Pallet Name': '', 'UPC': '744473001088',
         'Product Code': '21764', 'Brand': '@SODELICUS', 'Product Desc': 'SO DEL FRZN MOUSSE SALTD', 'Tax': '',
         'Whls. Cs. T': '41.33', 'Whls. Ea.': '5.1663', 'Reg SRP': '7.19', 'Weight': '3.86', 'Ext. Cube': '0.22',
         'Discount': '', 'Net - Case': '41.33', 'Net - Each': '5.1663', 'SRP': '7.19', 'Margin': '28',
         'Ext. Price': '41.33', 'Disc. Reas': ''},
    41: {'LN': '41', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/3 PK', 'Pallet Name': '', 'UPC': '794213000031',
         'Product Code': '70721', 'Brand': '@SSHINE', 'Product Desc': 'OG2 SSHINE GRDN HRB BRGR', 'Tax': '',
         'Whls. Cs. T': '52.98', 'Whls. Ea.': '4.4150', 'Reg SRP': '6.15', 'Weight': '7.90', 'Ext. Cube': '0.42',
         'Discount': '20%', 'Net - Case': '42.3840', 'Net - Each': '3.5320', 'SRP': '6.15', 'Margin': '43',
         'Ext. Price': '42.38', 'Disc. Reas': 'S'},
    42: {'LN': '42', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/10 OZ', 'Pallet Name': '', 'UPC': '638882000575',
         'Product Code': '77121', 'Brand': '@STAHLBUSH', 'Product Desc': 'STAHL RED RASPBERRIES', 'Tax': '',
         'Whls. Cs. T': '41.61', 'Whls. Ea.': '3.4675', 'Reg SRP': '4.79', 'Weight': '8.50', 'Ext. Cube': '0.42',
         'Discount': '27.83%', 'Net - Case': '30.0302', 'Net - Each': '2.5025', 'SRP': '4.79', 'Margin': '48',
         'Ext. Price': '30.03', 'Disc. Reas': 'FN'},
    43: {'LN': '43', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '12/10 OZ', 'Pallet Name': '', 'UPC': '638882000070',
         'Product Code': '77124', 'Brand': '@STAHLBUSH', 'Product Desc': 'STAHL BLUEBERRIES', 'Tax': '',
         'Whls. Cs. T': '41.61', 'Whls. Ea.': '3.4675', 'Reg SRP': '4.79', 'Weight': '8.30', 'Ext. Cube': '0.54',
         'Discount': '27.83%', 'Net - Case': '30.0302', 'Net - Each': '2.5025', 'SRP': '4.79', 'Margin': '48',
         'Ext. Price': '30.03', 'Disc. Reas': 'FN'},
    44: {'LN': '44', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/1 QT', 'Pallet Name': '', 'UPC': '784830100320',
         'Product Code': '78827', 'Brand': '@STRAUS', 'Product Desc': 'OG2 STRAUS VAN BEAN ICRM', 'Tax': '',
         'Whls. Cs. T': '40.39', 'Whls. Ea.': '6.7317', 'Reg SRP': '9.35', 'Weight': '13.00', 'Ext. Cube': '0.48',
         'Discount': '', 'Net - Case': '40.39', 'Net - Each': '6.7317', 'SRP': '9.35', 'Margin': '28',
         'Ext. Price': '40.39', 'Disc. Reas': ''},
    45: {'LN': '45', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '8/16 OZ', 'Pallet Name': '', 'UPC': '689076367943',
         'Product Code': '73710', 'Brand': '@THREETWIN', 'Product Desc': 'OG2 3TWN MOCHA DIFF ICRM', 'Tax': '',
         'Whls. Cs. T': '35.38', 'Whls. Ea.': '4.4225', 'Reg SRP': '6.15', 'Weight': '6.50', 'Ext. Cube': '0.23',
         'Discount': '', 'Net - Case': '35.38', 'Net - Each': '4.4225', 'SRP': '6.15', 'Margin': '28',
         'Ext. Price': '35.38', 'Disc. Reas': ''},
    46: {'LN': '46', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 52329 - UNFI DISCO', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    47: {'LN': '47', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'OG2 3TWN MADAGASCAR VAN', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    48: {'LN': '48', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': '', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '', 'Reg SRP': '', 'Weight': '',
         'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '', 'Margin': '\\r\\n',
         'Ext. Price': '', 'Disc. Reas': ''},
    49: {'LN': '49', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 75197 - MFG DISCO', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    50: {'LN': '50', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'E Z EDAMAME IN PODS', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    51: {'LN': '51', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': '', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '', 'Reg SRP': '', 'Weight': '',
         'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '', 'Margin': '\\r\\n',
         'Ext. Price': '', 'Disc. Reas': ''},
    52: {'LN': '52', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 06959 - MDISCO > 90', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    53: {'LN': '53', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'TCHEF SPN/PANR PZAS77500', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    54: {'LN': '54', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 - Refer to PN 77500*', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    55: {'LN': '55', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 Replacement shipped', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    56: {'LN': '56', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': '', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '', 'Reg SRP': '', 'Weight': '',
         'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '', 'Margin': '\\r\\n',
         'Ext. Price': '', 'Disc. Reas': ''},
    57: {'LN': '57', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'Q1 72395 - MFG DISCO', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    58: {'LN': '58', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': 'OG2 COBL STRAW LOVE BAR', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '',
         'Reg SRP': '', 'Weight': '', 'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '',
         'Margin': '\\r\\n', 'Ext. Price': '', 'Disc. Reas': ''},
    59: {'LN': '59', 'Ord': '', 'Shp': '', 'Eaches - Pack': '', 'Pallet Name': '', 'UPC': '', 'Product Code': 'REMRK',
         'Brand': '', 'Product Desc': '', 'Tax': '', 'Whls. Cs. T': '', 'Whls. Ea.': '', 'Reg SRP': '', 'Weight': '',
         'Ext. Cube': '', 'Discount': '', 'Net - Case': '', 'Net - Each': '', 'SRP': '', 'Margin': '\\r\\n',
         'Ext. Price': '', 'Disc. Reas': ''}}


class TestInvoiceScraper(TestCase):

    def setUp(self) -> None:
        from unfi_api_tests.assets import OrderManagementFiles
        order_management_files = OrderManagementFiles()
        self.invoice_html = order_management_files.orderhistory_GetCreditInvoiceDetailForWest

    def test_get_invoice_html_tables(self):
        """
        Test that the get_invoice_html_tables function returns dict of dics 
        """
        html = self.invoice_html
        tables = get_invoice_html_tables(html)
        self.assertIsInstance(tables, dict)

    def test_parse_table_with_labels_on_left(self):
        """
        Test that the parse_table_with_labels_on_left function returns a proper dict
        """
        table = [
            ["title"],
            ["label1", "value1"],
            ["label2", "value2"],
            ["", "value3"],
            ["label3", "value4"],
        ]
        returned_table = parse_table_with_labels_on_left(table)
        self.assertEqual(
            {'label1': 'value1', 'label2': 'value2\nvalue3', 'label3': 'value4'},
            returned_table
        )

    def test_index_line_item_table(self):
        """
        Test that the index_line_item_table function returns a proper dict
        """
        invoice_tables = get_invoice_html_tables(self.invoice_html)
        line_items_table = invoice_tables['line items']
        returned_data = index_line_item_table(line_items_table)
        pass

    def test_LineItem(self):
        li = {'LN': '1', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/6 PACK', 'Pallet Name': '', 'UPC': '028833041106',
              'Product Code': '16323', 'Brand': '#ALVARADO', 'Product Desc': 'OG3 ALV SPR ON/POPPY BAG', 'Tax': '',
              'Whls. Cs. T': '22.27', 'Whls. Ea.': '3.7117', 'Reg SRP': '5.15', 'Weight': '8.60', 'Ext. Cube': '0.64',
              'Discount': '', 'Net - Case': '22.27', 'Net - Each': '3.7117', 'SRP': '5.15', 'Margin': '28',
              'Ext. Price': '22.27', 'Disc. Reas': ''}
        line_item = LineItem(**li)
        pass

    def test_LineItem_each_size_no_slash(self):
        li = {'LN': '1', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '25 LB', 'Pallet Name': '', 'UPC': '028833041106',
              'Product Code': '16323', 'Brand': '#ALVARADO', 'Product Desc': 'OG3 ALV SPR ON/POPPY BAG', 'Tax': '',
              'Whls. Cs. T': '22.27', 'Whls. Ea.': '3.7117', 'Reg SRP': '5.15', 'Weight': '8.60', 'Ext. Cube': '0.64',
              'Discount': '', 'Net - Case': '22.27', 'Net - Each': '3.7117', 'SRP': '5.15', 'Margin': '28',
              'Ext. Price': '22.27', 'Disc. Reas': ''}
        line_item = LineItem(**li)
        self.assertEqual("25 LB", line_item.each_size)

    def test_LineItem_each_size_one_slash(self):
        li = {'LN': '1', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '6/16 oz', 'Pallet Name': '', 'UPC': '028833041106',
              'Product Code': '16323', 'Brand': '#ALVARADO', 'Product Desc': 'OG3 ALV SPR ON/POPPY BAG', 'Tax': '',
              'Whls. Cs. T': '22.27', 'Whls. Ea.': '3.7117', 'Reg SRP': '5.15', 'Weight': '8.60', 'Ext. Cube': '0.64',
              'Discount': '', 'Net - Case': '22.27', 'Net - Each': '3.7117', 'SRP': '5.15', 'Margin': '28',
              'Ext. Price': '22.27', 'Disc. Reas': ''}
        line_item = LineItem(**li)
        self.assertEqual("16 oz", line_item.each_size)
        self.assertEqual("6", line_item.case_size)

    def test_LineItem_each_size_two_slash(self):
        li = {'LN': '1', 'Ord': '1', 'Shp': '1', 'Eaches - Pack': '4/6/12 oz', 'Pallet Name': '', 'UPC': '028833041106',
              'Product Code': '16323', 'Brand': '#ALVARADO', 'Product Desc': 'OG3 ALV SPR ON/POPPY BAG', 'Tax': '',
              'Whls. Cs. T': '22.27', 'Whls. Ea.': '3.7117', 'Reg SRP': '5.15', 'Weight': '8.60', 'Ext. Cube': '0.64',
              'Discount': '', 'Net - Case': '22.27', 'Net - Each': '3.7117', 'SRP': '5.15', 'Margin': '28',
              'Ext. Price': '22.27', 'Disc. Reas': ''}
        line_item = LineItem(**li)
        self.assertEqual("6/12 oz", line_item.each_size)
        self.assertEqual("4", line_item.case_size)

    def test_many_line_items(self):
        """
        test to make sure it doesnt error out on the big list
        """
        for line in line_items_dict.values():
            # we wont ever be including a line item with blank ordered/shipped values these will be noted elsewhere
            if not line['Ord']:
                continue
            li = LineItem(**line)

