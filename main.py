import sys
import pandas as pd
from sqlalchemy import create_engine , exc
from Ing import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QLabel, QFrame,QComboBox,QGridLayout
from DataFrame import DfModel
from collections import Counter
from DynamiCombo import *
import datetime

class IngWindow ():

    def __init__(self):
        # initializing class with super privilege from parents classes
        super(IngWindow, self).__init__()
        self.main_page = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.first_page.setWindowTitle("Data Mapping ETL")
        self.df = []  # this is global within the class
        self.conn = ' '
        label_list = []
        b_label = ''
        f_label = ''
        # connecting button to functions
        print('lambda function entry')
        self.ui.home1_pushButton.clicked.connect(lambda: self.connecting_func('1'))
        self.ui.home2_pushButton.clicked.connect(lambda: self.connecting_func('2'))
        self.ui.home3_pushButton.clicked.connect(lambda: self.connecting_func('3'))
        self.ui.home4_pushButton.clicked.connect(lambda: self.connecting_func('4'))

    def connecting_func(self,a):
        print("connecting func")
        if a=='1':
            self.get_names('one')
            self.ui.home1_pushButton.clicked.connect(self.firstScreen)

        elif a=='2':
            self.get_names('two')
            self.ui.home2_pushButton.clicked.connect(self.firstScreen)

        elif a=='3':
            self.get_names('three')
            self.ui.home3_pushButton.clicked.connect(self.firstScreen)

        elif a=='4':
            self.get_names('four')
            self.ui.home4_pushButton.clicked.connect(self.firstScreen)


    def show(self):
        self.main_page.show()

    # defining function for closing button
    def exitapp(self):
        print("Exited")
        sys.exit()

    def firstScreen(self):
        print('first')
        self.ui.stackedWidget.setCurrentWidget(self.ui.first_page)
        self.ui.importButton.clicked.connect(self.importfile)
        self.ui.back_PushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home))
        self.ui.next_pushButton.clicked.connect(self.secondScreen)

    def get_names(self, a):
        print('get name')
        if a== 'one':
            self.ui.booking_label.setText(self.ui.booking1_label.text())
            self.ui.facility_label.setText(self.ui.facility1_label.text())
        elif a== 'two':
            self.ui.booking_label.setText(self.ui.booking2_label.text())
            self.ui.facility_label.setText(self.ui.facility2_label.text())
        elif a== 'three':
            self.ui.booking_label.setText(self.ui.booking3_label.text())
            self.ui.facility_label.setText(self.ui.facility3_label.text())
        elif a== 'four':
            self.ui.booking_label.setText(self.ui.booking4_label.text())
            self.ui.facility_label.setText(self.ui.facility4_label.text())

        print('get name last')


    # defining function for import button
    def importfile(self):
        #file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        filePath = QFileDialog.getOpenFileName()  # gives the file path
        path = str(filePath[0])
        print(path)
        if filePath[0] == '':
            return 0
        if path.endswith('.csv'):  # checks for file extension.
            df_read = pd.read_csv(str(path))

        else:
            print('in here')
            try:
               df_read = pd.read_excel(str(path))

               print('here')
            except Exception as e:
               print(e)
        model = DfModel(df_read)
        self.ui.tableView.setModel(model)
        self.df = df_read
        QMessageBox.about(self.main_page, 'Success', 'Congratulations! Your file is imported.')

    def db_connection(self):
        print("Database Connection Function")
        # this is used to fetch column name from the mysql database
        try:
            sql_engine = create_engine('mysql+pymysql://root:Lenovo12@127.0.0.1:3306/test', pool_recycle=3600)
            self.conn = sql_engine.connect()
            # self.conn = pymysql.connect(host='localhost', password='Lenovo12', db='test', user='root', port=3306)
        except BaseException as e:
            print(e)
            QMessageBox.about(self.main_page, 'Error in connection', str(e))
        #else:
            #QMessageBox.about(self.main_page, 'Congratulation', 'Database Connected Successful')

    def fetchColumnName(self):
        print(" fetchColumnName")
        # this function extracts the column names from the Database
        self.db_connection()
        result = self.conn.execute("select * from container ")
        column_list = []
        for col in result.keys():
            column_list.append(col)
        print(column_list)

        return [col for col in result.keys()]




    def secondScreen(self):
        print("second screen")
        self.ui.stackedWidget.setCurrentWidget(self.ui.second_page)
        # to display the table data in QtableView
        self.ui.tableView_2.clearSpans()
        model = DfModel(self.df)
        self.ui.tableView_2.setModel(model)
        # button function
        self.ui.backPushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.first_page))
        self.ui.next_push_button.clicked.connect(self.unknownContainerScreen)
        # db column names
        db_columns = self.fetchColumnName()
        df_list = list(self.df)
        lay1= self.ui.stackedWidget.findChild(QGridLayout, "gridLayout_2")
        global combo1
        combo1= add_widgets(self,db_columns, df_list, lay1)
        for index, i in enumerate(combo1):
            combo1[index].activated.connect(lambda: comboSelect(combo1))
            print(combo1[index].currentText())

        print(db_columns)



    def selected_df(self):
        print('selected df')
        # modifying the Dataframe with selected column names only
        data_frame1 = self.df
        index_df = comboSelect(combo1)  # getting the selected column names from combo boxes
        print(index_df)
        print("1111111111111111111111111111111111111111111111111111111")
        df1 = pd.DataFrame(data_frame1, columns=list(index_df))  # assigning selected columns ""values"" to new dataframe
        # changing the dataframe column names as database table column names
        print(df1)
        print('222222222222222222222222222222222222222222222222222222222')
        df1.columns = list(self.fetchColumnName())
        print('after changing column name')
        print(df1)
        return (df1)

    def fetch_unknown_container (self):
        print("fetch_unkown_container")
        # this provides a values and counts of the unknown containers in container type column
        selected_df = self.selected_df()
        container_value= selected_df["Container Type"].tolist()
        print(container_value)
        list_known = ["A1", 'B1', 'C1']
        list_unknown = []
        for a in container_value:
            if a not in list_known:
                list_unknown.append(a)
        my_dict = dict(Counter(list_unknown)) # saves container name as keys and its count as value
        key_list = list(my_dict.keys())
        values_list = list(my_dict.values())
        c = 0
        list1 = []
        for a in key_list:
            list1.append(str(a) + '(' + str(values_list[c]) + ')')
            c += 1
        print('3333333333333333333333333333333333333333')
        print(list1, key_list)
        print('444444444444444444444444444444444444444')
        return(list1, key_list)


    def unknownContainerScreen(self):
        print('third Screen')
        standard_containers = ["A1", "B1", "C1"]
        self.ui.stackedWidget.setCurrentWidget(self.ui.third_page)
        print('unkown here')
        unknown_list, values_list = self.fetch_unknown_container() # gives concatenated unknown container and its values

        lay1= self.ui.stackedWidget.findChild(QGridLayout,"gridLayout_9")
        #self.fetch_unknown_container()
        global combo_box
        combo_box = add_widgets(self, unknown_list, standard_containers, lay1)
        selected_index = []
        print('1111')
        print(combo_box)
        for index, i in enumerate(combo_box):
            combo_box[index].activated.connect(lambda: comboSelect(combo_box))
            print(combo_box[index].currentText())
        print('here')

        self.ui.unkown_back_pushbutton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.second_page))
        self.ui.unknown_next_pushButton.clicked.connect(self.selectedScreen)
        print('third end')


    def export_df(self):
        print("export_df")
        tableName = 'container'
        data_frame_db = self.selected_df()
        unknown_list, values_list = self.fetch_unknown_container()
        #selected_values = self.unknown_combo_select()
        selected_values = comboSelect(combo_box)
        data_frame_selected = data_frame_db.replace(values_list, selected_values)
        try:
            tableName = 'container'
            self.db_connection()
            data_frame_selected.to_sql(tableName, self.conn, index=False, if_exists='append')
            #QMessageBox.about(self.main_page, 'Success', 'Congratulations! Data is transferred to Database .')
        except ValueError as vx:
            print(vx)
            QMessageBox.about(self.main_page, 'Error in connection', str(vx))
        except exc.DBAPIError as ex:
            print(ex)
            QMessageBox.about(self.main_page, 'Error in insertion', str(ex))
        else:
            print("Table %s inserted successfully." % tableName);
            QMessageBox.about(self.main_page, 'Complete' , "Table %s inserted successfully." % tableName)
        finally:
            self.conn.close()

    def selectedStandardContainers(self):
        print("selectedStandardContainers()")
        # this changes the unknown containers types to standard ones chosen by user
        data_frame_db = self.selected_df()
        # change the unknown container to standard type
        unknown_list, values_list = self.fetch_unknown_container()
        #selected_values = self.unknown_combo_select()
        selected_values= comboSelect(combo_box)
        print(selected_values)
        data_frame_selected = data_frame_db.replace(values_list, selected_values)
        print(type(data_frame_selected))
        return data_frame_selected

    def selectedScreen(self):
        print("Selected Screen or fourth screen")
        # this shows the excel contain with standard selected containers. After choosing standard container type

        self.ui.stackedWidget.setCurrentWidget(self.ui.fourth_page)
        self.ui.tableView_excel.clearSpans()
        # showing original excel content
        model = DfModel(self.df)
        self.ui.tableView_excel.setModel(model)
        # showing the selected content
        self.ui.tableView_db.clearSpans()
        data_frame_selected = self.selectedStandardContainers()
        model2 = DfModel(data_frame_selected)
        self.ui.tableView_db.setModel(model2)
        print('fourrth here')
        # button function
        self.ui.back_pushbutton_s.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.third_page))
        self.ui.selected_next_pushButton.clicked.connect(self.finalTableView)

    def getTableData(self, data_frame1,selection):
        print("getTableData()")
        # this gets the count and  sum of container type as per year of manufacture
        df0 = pd.DataFrame(data_frame1, columns=['Date of Manufacture', 'Container Type'])
        df0['Count'] = 1
        df = df0.groupby(['Date of Manufacture', 'Container Type']).Count.count().reset_index()
        df1 = df.pivot(*df).fillna(0)
        grp = df1.groupby(pd.Grouper(freq='Y')).sum()
        if selection == '2':
            grp.loc[grp['A1'] > 0, 'A1'] *= 2
            grp.loc[grp['B1'] > 0, 'B1'] *= 3
            grp.loc[grp['C1'] > 0, 'C1'] *= 4

        grp1 = grp.reset_index(level="Date of Manufacture")
        print(grp1)
        grp1['Total'] = grp1['A1'] + grp1['B1'] + grp1['C1']
        grp1.loc['Total'] = grp1.sum(numeric_only=True, axis=0)
        grp1['Date of Manufacture'] = pd.to_datetime(grp1['Date of Manufacture']).dt.strftime('%Y')
        grp1.reset_index(drop=True, inplace=True)
        grp1.iloc[-1, grp1.columns.get_loc('Date of Manufacture')] = 'Total'
        print(grp1)
        return grp1

    def finalTableView(self):
        print('final Screen')
        self.ui.stackedWidget.setCurrentWidget(self.ui.fifth_page)
        df =self.selectedStandardContainers()
        table_df = self.getTableData(df,'1')
        model = DfModel(table_df)
        table_df1 = self.getTableData(df, '2')
        model1 = DfModel(table_df1)
        print ('final here')
        #self.ui.booking_label.setText('Sydney')
        #self.ui.facility_label.setText('Kilo')
        self.ui.unit_label.setText(str(int(table_df['Total'].iloc[-1])))
        self.ui.ceu_label.setText(str(int(table_df1['Total'].iloc[-1])))
        self.ui.yomunit_tableview.setModel(model)
        self.ui.ceu_tableview.setModel(model1)
        self.ui.confirm_export_pushbutton.clicked.connect(self.export_df)
        self.ui.gohome_pushbutton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.first_page))
        self.ui.cancel_pushbutton.clicked.connect(self.exitapp)
        print('Finallllyyyy')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_page = IngWindow()
    main_page.show()
    sys.exit(app.exec_())
