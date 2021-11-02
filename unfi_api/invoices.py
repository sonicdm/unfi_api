from .utils import index_header
from .utils.collections import find_most_common_member


class Invoice(object):
    """
    UNFI Invoice Worksheet Object
    """

    def __init__(self, invoice_sheet, invoice_number=None, date=None, inventory=None):
        """
        :param invoice_sheet: list of worksheet rows
        :param invoice_number: UNFI invoice number
        :param department: override the parsed department name
        :param date:
        """
        self.invoice_number = invoice_number
        self.invoice_sheet = invoice_sheet
        self.invoice_products = {}
        self.date = date
        self.invoice = None
        self.rows = {}
        self.inventory = inventory if inventory else None
        self.parse_invoice()

    def get_invoice_indexes(self, ws, header_row):
        colindex = index_header(ws, header_row)
        indexes = dict(
            upc=colindex['upc'][0],
            srp=colindex['reg srp'][0],
            size=colindex['eaches - pack'][0],
            ordered=colindex['ord'][0],
            shipped=colindex['shp'][0],
            desc=colindex['product desc'][0],
            cost=colindex['whls. cs. t'][0],
            prod_id=colindex['product code'][0],
        )
        return colindex, indexes

    def find_invoice_header(self, ws):
        for idx, row in enumerate(ws):
            if "UPC" in row:
                return idx
        return None

    def parse_invoice(self):
        """
        The guts of the invoice scraper.
        :return:
        """
        ws = self.invoice_sheet
        header_row = self.find_invoice_header(ws)
        colindex, indexes = self.get_invoice_indexes(ws, header_row)
        upcidx = indexes.get('upc')
        prodididx = indexes.get('prod_id')
        srpidx = indexes.get('srp')
        sizeidx = indexes.get('size')
        orderedidx = indexes.get('ordered')
        shippedidx = indexes.get('shipped')
        descidx = indexes.get('desc')
        invpackidx = indexes.get('size')
        costidx = indexes.get('cost')
        try:
            assert not any(idx is None for idx in [upcidx, srpidx, sizeidx, orderedidx, shippedidx, descidx])
        except AssertionError as e:
            print(e)
            raise AssertionError
        i = 1
        header = make_header(i)
        self.rows[i] = header
        for idx, row in enumerate(ws[header_row + 1:]):
            upc = row[upcidx]
            if len(str(upc)) > 13:
                upc = str(upc)[-13:]
            if upc:
                i += 1
                upc = int(stripcheckdigit(upc))
                prod_id = row[prodididx]
                invoice_pack = row[sizeidx]

                shipped = row[shippedidx]
                ordered = row[orderedidx]
                detail = ABBR.abbr_repl(row[descidx])
                if self.invoice_products.get(upc):
                    product = self.invoice_products.get(upc)
                elif self.inventory.inventory_products.get(upc):
                    product = self.inventory.inventory_products.get(upc)
                else:
                    product = Product(upc)
                product.invoice_pack = row[invpackidx]
                # product.srp = round_retails(srp)
                srp = row[srpidx]
                if isnumber(srp):
                    srp = float(row[srpidx])
                    product.srp = simple_round_retail(srp)
                cost = float(row[costidx]) if isnumber(row[srpidx]) else None
                product.ordered += int(ordered)
                product.shipped += int(shipped)
                product.invoice_number = self.invoice_number
                setattr(product, 'cost', cost)
                setattr(product, 'prod_id', prod_id)
                setattr(product, 'invoice_pack', invoice_pack)

                if product.retail and product.srp:
                    if product.retail != product.srp:
                        product.yellow = True

                if not product.detail:
                    product.detail = detail
                self.invoice_products[upc] = product
                if product.department:
                    self._departments.append(product.department)
                cells = build_cells(product)
                # Turn info into a row dict. This will all be better with excel wrapper. Perhaps this is a beta test.
                row = make_row(i, cells, product)
                self.rows[i] = row
