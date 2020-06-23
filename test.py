import runpy
from idCard import idRecognition

def test(filename, id, date):
    print("##### Test" + str(id) + " running: \x1b[6;30;47m" + filename + "\x1b[0m #####")
    result = idRecognition(filename)
    print("Test result: ", end="")
    if (result == None):
        print('\x1b[6;30;41m' + 'Failed !' + '\x1b[0m')
        return
    if (result[-1] == date):
        print('\x1b[6;30;42m' + 'Success !' + '\x1b[0m')
    else:
        print('\x1b[6;30;41m' + 'Failed !' + '\x1b[0m')

def main():
    #veronique
    test("Resources/img/veronique.jpg", 1, ['66', '07', '17'])
    test("Resources/img/veronique black and white.jpg", 3, ['66', '07', '17'])

    #dominique
    test("Resources/img/dominique.jpg", 4, ['63', '12', '25'])
    test("Resources/img/dominique.png", 6, ['63', '12', '25'])
    test("Resources/img/dominique black and white.jpg", 7, ['63', '12', '25'])


if __name__ == "__main__":
    main()