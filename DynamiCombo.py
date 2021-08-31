from PyQt5.QtWidgets import QWidget, QPushButton,QLabel,QComboBox, QGridLayout, QMainWindow, QFrame, QHBoxLayout, QVBoxLayout


def add_widgets(self, data1, data0, lay1):
    #global combos
    lay = lay1
    combos = []
    unknown_list = data1
    standard_containers= data0
    dict1 = dict(zip(unknown_list, standard_containers))
    for index, (key, value) in enumerate(dict1.items()):
        label = QLabel(key)
        combo = QComboBox()
        combo.addItems(data0)
        combos.append(combo)
        #setattr(self, 'combo%d' % index, combo)
        combo.setCurrentIndex(index)
        lay.addWidget(label, index, 0)
        lay.addWidget(combo, index, 1)
    return combos

def comboSelect(combos):

    # finding the current item index  in combo box
    combo_box= combos
    list_1=[]
    for index, combo in enumerate(combo_box):
        list_1.append(combos[index].currentText())
        item = combos[index].currentText()

    print(list_1)
    return(list_1)

