import runpy
from idCard import idRecognition

success = 0
failed = 0
nbTest = 1

def DateTest(filename, id, date):
    global success
    global failed
    global nbTest
    print("##### Test " + str(id) + " running: \x1b[6;30;47m" + filename + "\x1b[0m #####")
    result = idRecognition(filename)
    print("Test result: ", end="")
    if (result == None):
        print('\x1b[6;30;41m' + 'Failed !' + '\x1b[0m')
        failed += 1
        nbTest += 1
        return
    if (result[-1] == date):
        print('\x1b[6;30;42m' + 'Success !' + '\x1b[0m')
        success += 1
    else:
        print('\x1b[6;30;41m' + 'Failed !' + '\x1b[0m')
        failed += 1
    nbTest += 1

def main():
    global failed
    global success
    global nbTest
    #veronique
    DateTest("Resources/img/veronique.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/veronique black and white.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/testVal1.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/testVal4.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/testVal5 prenom incorrect.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/test14.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/test6.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/test7.jpg", nbTest, ['66', '07', '17'])
    DateTest("Resources/img/test10.jpg", nbTest, ['66', '07', '17'])

    #dominique
    DateTest("Resources/img/dominique.jpg", nbTest, ['63', '12', '25'])
    DateTest("Resources/img/dominique.png", nbTest, ['63', '12', '25'])
    DateTest("Resources/img/dominique black and white.jpg", nbTest, ['63', '12', '25'])

    #cecilia
    DateTest("Resources/img/cecilia.jpg", nbTest, ['91', '08', '30'])

    #emmanuel
    DateTest("Resources/img/emmanuel.jpg", nbTest, ['58', '06', '27'])
    DateTest("Resources/img/emmanuel.png", nbTest, ['58', '06', '27'])

    #romain
    DateTest("Resources/img/romain.pdf", nbTest, ['97', '05', '19'])
    DateTest("Resources/img/romain black and white.pdf", nbTest, ['97', '05', '19'])
    DateTest("Resources/img/test11.jpg", nbTest, ['97', '05', '19'])

    #pierre
    DateTest("Resources/img/pierre.jpg", nbTest, ['98', '05', '20'])
    DateTest("Resources/img/pierre.png", nbTest, ['98', '05', '20'])

    print('You have \x1b[6;30;41m' + str(failed) + '\x1b[0m' + ' \x1b[6;30;41m' + 'Failed' + '\x1b[0m and \x1b[6;30;42m' + str(success) + '\x1b[0m' + ' \x1b[6;30;42m' + 'Success' + '\x1b[0m for \x1b[6;30;47m' + str(nbTest - 1) + "\x1b[0m Tests" )


if __name__ == "__main__":
    main()