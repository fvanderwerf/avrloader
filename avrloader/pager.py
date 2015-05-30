
class Pager:
    def __init__(self, pagesize=32, filler='\xff'):
        self._pagesize = pagesize
        self._filler = filler

    def get_pageaddress(self, address):
        return address & ~(self._pagesize - 1)

    def pages(self, chunks):

        for chunk in chunks:
            address, data = chunk
            pageaddress = self.get_pageaddress(address)

            prefiller = (address - pageaddress) * self._filler

            address = pageaddress
            data = prefiller + data

            postfillersize = self._pagesize - (len(chunk[1]) % self._pagesize)
            if postfillersize != self._pagesize:
                postfiller = self._filler * postfillersize
            else:
                postfiller = ''

            data = data + postfiller

            assert (address % self._pagesize) == 0
            assert (len(data) % self._pagesize) == 0

            numpages = len(data) / self._pagesize

            for i in xrange(numpages):
                pageaddress = address + i * self._pagesize
                pagedata = data[pageaddress:pageaddress + self._pagesize]
                
                yield (pageaddress, pagedata)


