import runpy
from idCard import idRecognition

def test(filename, id, date):
    print("##### Test" + str(id) + " running: " + filename + " #####")
    result = idRecognition(filename)
    print("Test result: ", end="")
    if (result[-1] == date):
        print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    else:
        print(print('\x1b[6;30;41m' + 'Success!' + '\x1b[0m'))

def main():
    test("Resources/img/test.jpg", 1, ['66', '07', '17'])


if __name__ == "__main__":
    main()