
import bisect

class BinImage:
    def __init__(self):
        self._chunks = []

    def set(self, address, data):
        newchunk = (address, data)

        endaddress = address + len(data)

        pos = bisect.bisect(self._chunks, newchunk)

        if pos < len(self._chunks) and self._chunks[pos][0] == endaddress:
            # append trailing if they are contiguous
            newchunk = (address, data + self._chunks[pos][1])
            del self._chunks[pos]

        if pos - 1 >= 0:
            precedingChunk = self._chunks[pos - 1]
            endaddressOfPrecedingChunk = precedingChunk[0] + len(precedingChunk[1])
            if endaddressOfPrecedingChunk == address:
                # prepend preceding chunk if they are contiguous
                newchunk = (precedingChunk[0], precedingChunk[1] + newchunk[1])
                del self._chunks[pos - 1]
                pos = pos - 1

        self._chunks.insert(pos, newchunk)

    def dump(self):
        for chunk in self._chunks:
            print chunk[0], ':', chunk[1].encode('hex')

    def get_chunks(self):
        return self._chunks


class Pager:
    def __init__(self, pagesize):
        self._pagesize = pagesize

    def page(self, chunks):
        for chunk in chunks:
            pass
