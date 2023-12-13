import heapq

class HuffmanNode:
    def __init__(self, char, frequency):
        # Инициализация узла Хаффмана с символом и частотой
        self.char = char #Символ узла
        self.frequency = frequency #Частота появления символа в тексте
        self.left = None #Левый потомок в дереве
        self.right = None #Правый потомок в дереве

    def __lt__(self, other):
        # Метод сравнения для сортировки узлов в куче
        return self.frequency < other.frequency

def build_huffman_tree(text):
    # Построение дерева Хаффмана на основе частот символов в тексте
    frequency_map = {}
    for char in text:
        frequency_map[char] = frequency_map.get(char, 0) + 1

    # Инициализация кучи с узлами Хаффмана
    heap = [HuffmanNode(char, freq) for char, freq in frequency_map.items()]
    heapq.heapify(heap)

    # Слияние узлов до построения полного дерева
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.frequency + right.frequency)
        merged.left, merged.right = left, right
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, code="", mapping=None):
    # Рекурсивное построение кодов Хаффмана для каждого символа
    if mapping is None:
        mapping = {}

    if node is not None:
        if node.char is not None:
            mapping[node.char] = code
        build_huffman_codes(node.left, code + "0", mapping)
        build_huffman_codes(node.right, code + "1", mapping)

    return mapping

def compress(text, output_filename):
    # Сжатие текста методом Хаффмана
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)

    # Кодирование текста
    encoded_text = ''.join(codes[char] for char in text)
    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding

    # Конвертация в байты
    bytes_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = int(encoded_text[i:i + 8], 2)
        bytes_array.append(byte)

    # Запись в бинарный файл
    with open(output_filename, 'wb') as compressed_file:
        compressed_file.write(bytes_array)

    print(f'Сжатие завершено. Результат записан в файл {output_filename}')