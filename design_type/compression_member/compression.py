"""

@Author:    Rutvik Joshi - Osdag Team, IIT Bombay [(P) rutvikjoshi63@gmail.com / 30005086@iitb.ac.in]

@Module - Compression Member
@Sub Module - Strut in a Truss


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               4) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)
                     
other          8) 
references     9)

"""
# noinspection PyInterpreter
from design_type.member import Member
from Common import *
from utils.common.component import ISection, Material
from utils.common.common_calculation import *
from utils.common.load import Load
from design_type.tension_member import *
from utils.common.Section_Properties_Calculator import BBAngle_Properties
import math
import numpy as np
from utils.common import is800_2007
from utils.common.component import *
from design_report.reportGenerator_latex import CreateLatex



class Compression(Member):

    def __init__(self):
        # print(f"Here Compression")
        super(Compression, self).__init__()

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layoutGusset Plate Details

        """
        tabs = []

        t1 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_strut_angle_section)
        tabs.append(t1)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_strut_channel_section)
        # tabs.append(t2)

        t2 = ("Optimization", TYPE_TAB_2, self.optimization_tab_strut_design)
        tabs.append(t2)
        
        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).
         TODO: input widget type of keys (3rd element) is no longer required. needs to be removed
         """
        change_tab = []

        t1 = (DISP_TITLE_ANGLE, [KEY_SECSIZE, KEY_SEC_MATERIAL,'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
               'Label_7', 'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', 'Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_strut_angle_section_properties)
        change_tab.append(t1)

        t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3','Label_0'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
               KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Strut_Angle_sec_properties)
        change_tab.append(t2)

        # t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
        #       [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14',
        #        'Label_4', 'Label_5',
        #        'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
        #        'Label_19', 'Label_20', 'Label_21',
        #        'Label_22', 'Label_23', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
        #       self.get_new_channel_section_properties)
        # change_tab.append(t3)
        #
        # t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14'],
        #       ['Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17', 'Label_19',
        #        'Label_20', 'Label_21', 'Label_22', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
        #       self.get_Channel_sec_properties)
        #
        # change_tab.append(t4)

        # t5 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
        #                                               KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        #
        # change_tab.append(t5)

        t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        # t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        # change_tab.append(t7)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        # t2 = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        # design_input.append(t2)

        t2 = ("Optimization", TYPE_TEXTBOX, [KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane, KEY_BOLT_Number ]) #KEY_ALLOW_UR, , KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Optimization", TYPE_COMBOBOX, [KEY_ALLOW_CLASS, KEY_ALLOW_LOAD, Load_type2, Load_type1, KEY_PLATETHK ]) # KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS,
        design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        # t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        # design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to
        design dictionary if design preference is never opened by user. It sets are design preference values to default.
        If any design preference value needs to be set to input dock value, tuple shall be written as:

        (Key of input dock, [List of Keys from design prefernce], 'Input Dock')

        If the values needs to be set to default,

        (None, [List of Design Prefernce Keys], '')

         """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_ALLOW_CLASS, KEY_ALLOW_UR, KEY_EFFECTIVE_AREA_PARA, KEY_Buckling_Out_plane, KEY_Buckling_In_plane,
                     KEY_DP_DESIGN_METHOD, KEY_ALLOW_LOAD, KEY_BOLT_Number, KEY_PLATETHK
                     ], '')#, KEY_OPTIMIZATION_PARA, KEY_ALLOW_CLASS, KEY_STEEL_COST, KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_EDGE_TYPE,KEY_DP_DETAILING_GAP,
                     # KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_CONNECTOR_MATERIAL , KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
        design_input.append(t2)

        # t2 = (None, [KEY_DP_DESIGN_METHOD], '')
        # design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []
# TODO
        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              VALUES_SEC_PROFILE_Compression_Strut , Profile_name_1)
        add_buttons.append(t2)

        # t2 = (DISP_TITLE_CHANNEL, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
        #       ['Channels', 'Back to Back Channels'], "Channels")
        # add_buttons.append(t2)

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            material = Material(design_dictionary[KEY_MATERIAL], 41)
            fu = material.fu
            fy = material.fy
        else:
            fu = ''
            fy = ''

        val = {
            KEY_ALLOW_UR: '1.0',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_ALLOW_CLASS : 'Yes',
            KEY_Buckling_Out_plane: '1.0',
            KEY_Buckling_In_plane: '1.0',
            KEY_ALLOW_LOAD: Load_type1,
            KEY_BOLT_Number: '1.0',
            KEY_ALLOW_LOAD: 'Concentric Load',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_PLATETHK : '8'
        }[key]

        return val

    ####################################
    # Design Preference Functions End
    ####################################

    def module_name(self):
        return KEY_DISP_COMPRESSION_STRUT

    def set_osdaglogger(key):

        """
        Function to set Logger for Strut design Module
        """

        # @author Rutvik J
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        # handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        if key is not None:
            handler = OurLog(key)
            # handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def customized_input(self):

        c_lst = []

        t1 = (KEY_SECSIZE, self.fn_profile_section)
        c_lst.append(t1)
        # t2 = (KEY_GRD, self.grdval_customized)
        # c_lst.append(t2)
        # t3 = (KEY_D, self.diam_bolt_customized)
        # c_lst.append(t3)
        # # # t3= (KEY_IMAGE, self.fn_conn_image)
        # # # c_lst.append(t3)
        # t4 = (KEY_PLATETHK, self.plate_thick_customized_IS)
        # c_lst.append(t4)

        # t4 = (KEY_PLATETHK, self.plate_thick_customized)
        # c_lst.append(t4)

        return c_lst

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''

        # @author: Amir, Umair

        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_COMPRESSION_Strut, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (None, KEY_SECTION_DATA, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE_Compression_Strut, True, 'No Validator')
        options_list.append(t2)

        # print(f'input_values {self},t2 :{t2} ')
        # if self[0] == 'Back to Back Angles':
        #     t2 = (KEY_SEC_TYPE, KEY_DISP_SEC_TYPE, TYPE_COMBOBOX, ['Same Side of Gusset', 'Opposite Side of Gusset'], True,
        #           'No Validator')
        #     options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, VALUES_IMG_STRUT[0], True, 'No Validator')
        options_list.append(t3)

        t3 = (KEY_LOCATION, KEY_DISP_LOCATION_STRUT, TYPE_COMBOBOX, VALUES_LOCATION_1, True, 'No Validator')
        options_list.append(t3)

        # ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, ['All','Customized'], True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t9 = (None, DISP_TITLE_STRUT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_END1, KEY_DISP_END1, TYPE_COMBOBOX, VALUES_STRUT_END1, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_END2, KEY_DISP_END2, TYPE_COMBOBOX, VALUES_STRUT_END2, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_IMAGE_two, None, TYPE_IMAGE_COMPRESSION, "./ResourceFiles/images/6.RRRR.PNG", True, 'No Validator')
        options_list.append(t12)

        t7 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        return options_list

    def memb_pattern(self, status):

        if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
            image = './ResourceFiles/images/L.png'
            x, y = 400, 202

        else:
            image = './ResourceFiles/images/U.png'
            x, y = 400, 202


        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_IMAGE,
               [image, x, y, "Member Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        return pattern

    def plate_pattern(self, status):

        pattern = []

        t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
        pattern.append(t00)

        t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
               ['./ResourceFiles/images/L.png',400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
        pattern.append(t99)

        return pattern

    def fn_end1_end2(self):

        end1 = self[0]
        if end1 == 'Fixed':
            return VALUES_STRUT_END2
        elif end1 == 'Free':
            return ['Fixed']
        elif end1 == 'Hinged':
            return ['Fixed', 'Hinged']
        elif end1 == 'Roller':
            return ['Fixed', 'Hinged']

    def fn_end1_image(self):

        if self == 'Fixed':
            return "./ResourceFiles/images/6.RRRR.PNG"
        elif self == 'Free':
            return "./ResourceFiles/images/1.RRFF.PNG"
        elif self == 'Hinged':
            return "./ResourceFiles/images/5.RRRF.PNG"
        elif self == 'Roller':
            return "./ResourceFiles/images/4.RRFR.PNG"

    def fn_end2_image(self):

        end1 = self[0]
        end2 = self[1]

        if end1 == 'Fixed':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/6.RRRR.PNG"
            elif end2 == 'Free':
                return "./ResourceFiles/images/1.RRFF_rotated.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/5.RRRF_rotated.PNG"
            elif end2 == 'Roller':
                return "./ResourceFiles/images/4.RRFR_rotated.PNG"
        elif end1 == 'Free':
            return "./ResourceFiles/images/1.RRFF.PNG"
        elif end1 == 'Hinged':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/5.RRRF.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/3.RFRF.PNG"
            elif end2 == 'Roller':
                return "./ResourceFiles/images/2.FRFR_rotated.PNG"
        elif end1 == 'Roller':
            if end2 == 'Fixed':
                return "./ResourceFiles/images/4.RRFR.PNG"
            elif end2 == 'Hinged':
                return "./ResourceFiles/images/2.FRFR.PNG"

    def fn_conn_image(self):

        "Function to populate section images based on the type of section "
        img = self[0]
        if img == VALUES_SEC_PROFILE_Compression_Strut[0]:
            return VALUES_IMG_STRUT[0]
        elif img ==VALUES_SEC_PROFILE_Compression_Strut[1]:
            return VALUES_IMG_STRUT[2]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[2]:
            return VALUES_IMG_STRUT[1]
        elif img == VALUES_SEC_PROFILE_Compression_Strut[3]:
            print(' fn_conn_image error')
            return VALUES_IMG_TENSIONBOLTED[3]
        else:
            return VALUES_IMG_TENSIONBOLTED[4]


    def fn_profile_section(self):
        #print(f"fn_profile_section self {self}")
        profile = self[0]
        # print(f'profile = {self[0]}'
        #       f'VALUES_SEC_PROFILE_Compression_Strut {VALUES_SEC_PROFILE_Compression_Strut}')
        if profile == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif profile == 'Columns':
            return connectdb("Columns", call_type="popup")
        elif profile == 'RHS':
            return connectdb("RHS", call_type="popup")
        elif profile == 'SHS':
            return connectdb("SHS", call_type="popup")
        elif profile == 'CHS':
            return connectdb("CHS", call_type="popup")
        elif profile in VALUES_SEC_PROFILE_Compression_Strut :
            # print('done')
            return connectdb("Angles", call_type="popup")
        elif profile in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type="popup")


    def input_value_changed(self):

        lst = []

        t1 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t1)

        # if self[0] == 'Back to Back Angles':

        t3 = ([KEY_SEC_PROFILE], KEY_LOCATION, TYPE_COMBOBOX, self.fn_conn_type)
        lst.append(t3)

        t3 = ([KEY_SEC_PROFILE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t3)

        t2 = ([KEY_END1], KEY_END2, TYPE_COMBOBOX, self.fn_end1_end2)
        lst.append(t2)

        t3 = ([KEY_END1, KEY_END2], KEY_IMAGE_two, TYPE_IMAGE, self.fn_end2_image)
        lst.append(t3)

        return lst

    def output_values(self,flag):
        #flag for design status
        out_list = []
        # if flag is True:
        #     if self.input_values is not VALUE_NOT_APPLICABLE:
        #         # print(f"input_values is not VALUE_NOT_APPLICABLE")
        #     else:
        #         # print(f"input_values is VALUE_NOT_APPLICABLE")
        t1 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)

        out_list.append(t1)

        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX, self.result_designation if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, self.result_UR if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.result_section_class if flag else '', True)
        out_list.append(t1)

        t2 = (KEY_EFF_SEC_AREA, KEY_DISP_EFF_SEC_AREA, TYPE_TEXTBOX, round(self.result_effective_area, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EFF_LEN, KEY_DISP_EFF_LEN, TYPE_TEXTBOX, round(self.result_eff_len, 2) if flag else '',
        True)
        out_list.append(t2)

        t2 = (KEY_ESR, KEY_DISP_ESR, TYPE_TEXTBOX, round(self.result_eff_sr, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_lambdavv, KEY_DISP_SR_lambdavv, TYPE_TEXTBOX, self.result_lambda_vv if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_lambdapsi, KEY_DISP_SR_lambdapsi, TYPE_TEXTBOX, self.result_lambda_psi if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_EULER_BUCKLING_STRESS, KEY_DISP_EULER_BUCKLING_STRESS, TYPE_TEXTBOX, round(self.result_ebs, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_BUCKLING_CURVE, KEY_DISP_BUCKLING_CURVE, TYPE_TEXTBOX, self.result_bc if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_IMPERFECTION_FACTOR, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, round(self.result_IF, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, round(self.result_srf, 2) if flag else '', True)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, round(self.result_nd_esr, 2) if flag else '', True)
        out_list.append(t2)

        t1 = (None, KEY_DESIGN_COMPRESSION, TYPE_TITLE, None, True)
        out_list.append(t1)

        t1 = (KEY_COMP_STRESS, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              round(self.result_fcd * 1e-3, 2) if flag else
              '', True)
        out_list.append(t1)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_DESIGN_STRENGTH_COMPRESSION, TYPE_TEXTBOX, round(self.result_capacity * 1e-3, 2) if flag else
        '', True)
        out_list.append(t1)

        return out_list
    def func_for_validation(self, design_dictionary):
        '''Need to check'''
        all_errors = []
        self.design_status = False
        flag = False
        self.output_values(self, flag)
        flag1 = False
        flag2 = False
        flag3 = False
        option_list = self.input_values(self)
        print(f'\n func_for_validation ' #option list = {option_list}
              f'\n  design_dictionary {design_dictionary}')
        missing_fields_list = []
        print(f'func_for_validation option_list {option_list}'
            f"\n  design_dictionary {design_dictionary}"
              )
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                # print(f"\n option {option}")
                if design_dictionary[option[0]] == '' and option[0] is not KEY_AXIAL:
                    # print(f'option, design_dictionary[option[0] = {option[0]},{design_dictionary[option[0]]}')
                    # if design_dictionary[KEY_AXIAL] == '':
                    #     continue
                    # else:
                    missing_fields_list.append(option[1])
                elif design_dictionary[option[0]] == '' and option[0] is KEY_AXIAL:
                    flag2 = True
                else:
                    if option[0] == KEY_LENGTH :
                        if float(design_dictionary[option[0]]) <= 0.0:
                            # print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag1 = True
                    elif option[0] == KEY_AXIAL :
                        try:
                            if float(design_dictionary[option[0]]) <= 0.0:
                                #print("Input value(s) cannot be equal or less than zero.")
                                error = "Input value(s) cannot be equal or less than zero."
                                all_errors.append(error)
                            else:
                                flag2 = True
                        except:
                            error = "Input value(s) are not valid"
                            all_errors.append(error)
                            
            elif option[2] == TYPE_COMBOBOX and option[0] not in [KEY_SEC_PROFILE, KEY_END1, KEY_END2, KEY_LOCATION, KEY_TYP]:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    # print(f'option[0] = {option[0]}')
                    missing_fields_list.append(option[1])
            elif option[0] == KEY_SEC_PROFILE:
                if design_dictionary[option[0]] not in VALUES_SEC_PROFILE_Compression_Strut:
                    return 'Provide any Angle section'
                else:
                    flag3 = True
        # print(missing_fields_list)
        if len(missing_fields_list) > 0:

            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        #print(f'flag = {flag}')
        if flag and flag1 and flag2 and flag3:
            self.set_input_values(self, design_dictionary)
            # print(design_dictionary)
            if self.design_status ==False :# and len(self.failed_design_dict)>0:
                logger.error(
                    "Design Failed, Check Design Report"
                )
                return # ['Design Failed, Check Design Report'] @TODO
            elif self.design_status:
                pass
            else:
                logger.error(
                    "Design Failed. Slender Sections Selected"
                )
                return 
            # ['Design Failed. Selender Sections Selected']
        else:
            return all_errors
        print(f"func_for_validation done")

    def fn_conn_type(self):

        "Function to populate section size based on the type of section "
        conn = self[0]
        if conn in VALUES_SEC_PROFILE_Compression_Strut:
            return VALUES_LOCATION_1
        else:
            print(f" check fn_conn_type ")

    # Setting inputs from the input dock GUI

    def set_input_values(self, design_dictionary):
        super(Compression,self).set_input_values(self, design_dictionary)
        self.mainmodule = KEY_DISP_COMPRESSION_STRUT
        self.module = design_dictionary[KEY_MODULE]
        self.sizelist = design_dictionary[KEY_SECSIZE]
        self.sec_profile = design_dictionary[KEY_SEC_PROFILE]
        self.sec_list = design_dictionary[KEY_SECSIZE]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.main_material = design_dictionary[KEY_MATERIAL]
        self.material = design_dictionary[KEY_SEC_MATERIAL]
        # try :
        self.in_plane = float(design_dictionary[KEY_Buckling_In_plane])
        self.out_plane = float(design_dictionary[KEY_Buckling_Out_plane])
        if KEY_BOLT_Number not in design_dictionary:
            self.bolts = 0.0
        else:
            self.bolts = float(design_dictionary[KEY_BOLT_Number])

        if KEY_PLATETHK not in design_dictionary:
            self.plate_thickness = 0.0
        else:
            # Gusset plate details
            self.plate_thickness = float(design_dictionary[KEY_PLATETHK])

        # self.plate_grade = design_dictionary[KEY_SEC_MATERIAL]
        print(f"plate_thickness {self.plate_thickness} \n"
            f"self.in_plane {self.in_plane} \n"
              f"self.out_plane {self.out_plane} \n"
              f"self.bolts {self.bolts} \n"
            "========Unknown keys==========")
        print("character",[chr(code) for code in range(945,970)])


        #'Conn_Location'
        self.loc = design_dictionary[KEY_LOCATION]


        # self.load_type = 'Concentric Load'


        # end condition
        self.end_1 = design_dictionary[KEY_END1]
        self.end_2 = design_dictionary[KEY_END2]
        if self.end_1 == 'Fixed' and self.end_2 == 'Fixed':
            self.fixity = 'Fixed'
        elif (self.end_1 == 'Fixed' and self.end_2 == 'Hinged') or (self.end_1 == 'Hinged' and self.end_2 == 'Fixed') :
            self.fixity = 'Partial'
        else:
            self.fixity = 'Hinged'

        # 'Bolt.Diameter'
        # self.bolt_list = design_dictionary[KEY_D]
        # self.bolt_type = design_dictionary[KEY_TYP]
        # self.bolt_grade = design_dictionary[KEY_GRD]
        # print(f"bolt_list {self.bolt_list}")


        # factored loads
        self.load = Load(shear_force="", axial_force=design_dictionary[KEY_AXIAL],moment="",unit_kNm=True)

        # design preferences
        self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        self.optimization_parameter = 'Utilization Ratio'
        self.allow_class = design_dictionary[KEY_ALLOW_CLASS] #'Semi-Compact' # @TODO
        self.load_type = design_dictionary[KEY_ALLOW_LOAD]
        # ['Concentric Load', 'Leg Load']
        # if self.sec_profile == 'Angles':
        self.load_type = design_dictionary[KEY_ALLOW_LOAD]
        # else:
        #     self.load_type = 'Concentric Load'
        self.steel_cost_per_kg = 50
        #
        # print(f"set_input_values design_dictionary {design_dictionary}")
        # print(f"set_input_values self.module {self.module}")
        # print(f"set_input_values self.sec_profile {self.sec_profile}")
        # print(f"set_input_values self.material {self.material}")
        # print(f"set_input_values self.load {self.load}")

        self.allowed_sections = []

        if self.allow_class == "Yes":
            self.allowed_sections.append('Semi-Compact')
            # print(f"Allowed Semi-Compact")
        '''Need to check'''
        # if self.allow_class4 == "Yes":
        #     self.allowed_sections.append('Slender')

        print(f"self.allowed_sections {self.allowed_sections} \n"
        "================== \n"
        f"self.load_type {self.load_type} \n"
        f"self.module{self.module} \n"
        f"self.sec_list {self.sec_list} \n"
        f"self.material {self.material} \n"
        f"self.length {self.length} \n"
        f"self.load {self.load} \n"
        f"self.end_1,2 {self.end_1}, {self.end_2} \n"
        "==================")

        # safety factors
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        # material property
        self.material_property = Material(material_grade=self.material, thickness=0)
        # print(f"self.material_property {self.material_property}]")


        # initialize the design status
        self.design_status_list = []
        self.design_status = False

        #initial properties of section
        self.sec_prop_initial_dict = {}

        # self.results(self)

        # "Unknown keys"
        # if self.sec_profile == Profile_name_1 :
        self.K = self.in_plane * self.out_plane
        self.K = self.K * IS800_2007.cl_7_2_2_effective_length_of_prismatic_compression_members(
            self.length,
            end_1=self.end_1,
            end_2=self.end_2) / self.length

        # 2.2 - Effective length

        self.effective_length = self.K * self.length  # IS800_2007.cl_7_2_4_effective_length_of_truss_compression_members(self.length,self.sec_profile)/ self.length  # mm
        print(f"self.effective_length {self.effective_length} ")
        # elif self.sec_profile == 'Back to Back Angles':
        #     self.K = 0.85
        # elif self.sec_profile == 'Channels':
        #     print("========Unknown keys==========")
        #     self.K = 0.85
        # elif self.sec_profile == 'Back to Back Channels':
        #     print("========Unknown keys==========")
        #     self.K = 0.85

        # self.count = 0
        # self.member_design_status = False
        # self.max_limit_status_1 = False
        # self.max_limit_status_2 = False
        # self.bolt_design_status = False
        # self.plate_design_status = False
        # self.inter_status = False
        # self.thk_count =0

        print("K = {}.\n The input values are set. Performing preliminary member check(s).".format(self.K))
        # self.i = 0
        # checking input values
        flag = self.section_classification(self)
        if flag:
            self.design(self, design_dictionary)
            self.results(self, design_dictionary)

    def get_3d_components(self):

        components = []
        return components

    def section_classification(self):
        # print(f"Inside section_classification")
        local_flag = False
        self.input_section_list = []
        self.input_section_classification = {}

        for section in self.sec_list:
            trial_section = section.strip("'")
            # fetching the section properties
            self.section_property = self.section_connect_database(self,trial_section)

            # section classification
            if (self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[:3]):  # Angles or Back to Back or 'Star Angle'

                # updating the material property based on thickness of the thickest element
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.thickness)
                if self.section_property.type == 'Rolled':
                    if self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[0] or self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[2]:
                        self.section_property.section_class, self.width_thickness_ratio, self.depth_thickness_ratio, self.width_depth_thickness_ratio = IS800_2007.Table2_vi(self.section_property.min_leg, self.section_property.max_leg, self.section_property.thickness,
                                                            self.material_property.fy, "Axial Compression")
                    elif self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]:
                        self.section_property.section_class, self.width_thickness_ratio, self.depth_thickness_ratio, self.width_depth_thickness_ratio = IS800_2007.Table2_vii(self.section_property.min_leg,
                                                              self.section_property.max_leg,
                                                              self.section_property.thickness,
                                                              self.material_property.fy, "Axial Compression")
                    # print(f"\n \n \n self.material_property.fy {self.material_property.fy} \n \n \n")
                    # self.section_property.section_class = list_Table2_vi[0]
                    # self.width_thickness_ratio  = list_Table2_vi[1]
                    # self.depth_thickness_ratio = list_Table2_vi[2]
                    # self.width_depth_thickness_ratio = list_Table2_vi[3]
                    #print(f"DONE {self.section_property.section_class} {self.width_thickness_ratio} {self.depth_thickness_ratio} {self.width_depth_thickness_ratio}")
                    # @TODO add to dictionary to print as log message
                    # if self.section_property.section_class != 'Slender':
                    #     logger.info(
                    #         "The section is {}. The b/t of the trial section ({}) is {} and d/t is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                    #             self.section_property.section_class, trial_section,
                    #             round(self.width_thickness_ratio, 2), round_up(self.depth_thickness_ratio),
                    #             round(self.width_depth_thickness_ratio, 2)))
                    # else:
                    #     logger.warning(
                    #         "The section is {}. The b/t of the trial section ({}) is {} and d/t is {} and (b+d)/t is {}.  [Reference: Cl 3.7, IS 800:2007].".format(
                    #             self.section_property.section_class, trial_section,
                    #             round(self.width_thickness_ratio, 2), round_up(self.depth_thickness_ratio),
                    #             round(self.width_depth_thickness_ratio, 2)))
                    #     logger.warning("Ignoring section")


                else:
                    print(f"section_classification _ not done")
                    local_flag = False
            elif (self.sec_profile in ['Channels', 'Back to Back Channels']):
                # updating the material property based on thickness of the thickest element
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.web_thickness)

                list_Table2_iv = IS800_2007.Table2_iv(depth=self.section_property.depth, f_y=self.material_property.fy, thickness_web= self.section_property.web_thickness)
                print(f"Checking Channel Properties")
                self.section_property.section_class = list_Table2_iv[0]
                self.depth_thickness_ratio = list_Table2_iv[1]
                logger.info("The section is {}. The d/t_web of the trial section ({}) is {}.  [Reference: Cl 3.7, IS 800:2007].".format(self.section_property.section_class, trial_section, round(self.depth_thickness_ratio,2) ))
            else:
                print(f"section_classification _ cannot do")
                local_flag = False


            # 2.3 - slenderness ratio
            if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:
                min_radius_gyration, effective_area = self.min_rad_gyration_calc_strut(self,designation= self.section_property.designation, material_grade=self.material,
                                           key=self.sec_profile, subkey=self.loc, D_a=self.section_property.a,
                                           B_b=self.section_property.b, T_t=self.section_property.thickness, t = self.plate_thickness)
            
            slenderness = self.design_check_for_slenderness(self,K= self.K, L = self.length*1000, r = min_radius_gyration)#(self.effective_length / self.min_radius_gyration)

            print(f"min_radius_gyration {min_radius_gyration},self.K = {self.K}, self.length = {self.length}"
                  f"slenderness {slenderness}")
            limit = IS800_2007.cl_3_8_max_slenderness_ratio(1)
            if slenderness > limit:
                local_flag = False
            else:
                local_flag = True
            # if len(self.allowed_sections) == 0 or len(self.sec_list) == 0:
            #     logger.warning("Select at-least one type of section in the design preferences tab.")
            #     logger.error("Cannot compute. Selected section classification type is Null.")
            #     self.design_status = False
            #     self.design_status_list.append(self.design_status)
            #     local_flag = False

            if self.section_property.section_class in self.allowed_sections and local_flag == True:
                self.input_section_list.append(trial_section)
                self.input_section_classification.update({trial_section: self.section_property.section_class})
                self.sec_prop_initial_dict.update({trial_section : (self.section_property.section_class, min_radius_gyration, slenderness, effective_area)}) #, self.width_thickness_ratio,self.depth_thickness_ratio,self.width_depth_thickness_ratio
        
        if len(self.input_section_list) == 0:
            local_flag = False
            logger.warning("Length provided is beyond the limit allowed. [Reference: Cl 3.8, IS 800:2007]")
            logger.error("Cannot compute. Given Length does not pass for this section.")
        else:
            local_flag = True
            logger.info("Length provided is within the limit allowed. [Reference: Cl 3.8, IS 800:2007]" )

        return local_flag

    #  ======Calculations start here====== #
    def optimization_tab_check(self):
        if (self.allowable_utilization_ratio <= 0.10) or (self.allowable_utilization_ratio > 1.0):
            logger.warning(
                "The defined value of Utilization Ratio in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.allowable_utilization_ratio = 1.0
            # self.design_status = False
            # self.design_status_list.append(self.design_status)

        elif (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.warning(
                "The defined value of Effective Area Factor in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            # self.design_status = False
            # self.design_status_list.append(self.design_status)

        elif (self.steel_cost_per_kg < 0.10) or (self.effective_area_factor > 1.0):
            # No suggested range in Description
            logger.warning(
                "The defined value of the cost of steel (in INR) in the design preferences tab is out of the suggested range.")
            logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default rate of 50 (INR/kg).")
            self.steel_cost_per_kg = 50
            self.design_status = False
            self.design_status_list.append(self.design_status)
        else:
            logger.info("Provided appropriate design preference, now checking input.")

    def section_connect_database(self, section):
        if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:  # Angles
            self.section_property = Angle(designation = section, material_grade = self.material)
        else:
            logger.warning(
                "The section should be either Angle or Back to Back Angle. ")
            
        if self.sec_profile == Profile_name_1 or self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3:
                # self.material_property(self.material, self.section_property.thickness)
                self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.thickness)
        elif self.sec_profile in ['Channels', 'Back to Back Channels']:
            self.material_property.connect_to_database_to_get_fy_fu(self.material, self.section_property.web_thickness)
        self.epsilon = math.sqrt(250 / self.material_property.fy)
            
        return self.section_property

    def common_checks_1(self, section, step = 1, list_result = [], list_1 = []):
        if step == 1:
            # print(f"Working correct here{section}")
            print(section)
            print(self.sec_profile)

            # fetching the section properties of the selected section
            self.section_connect_database(self, section)
            

            # print(f"Working correct here")
        elif step == 2:
            if self.section_property.section_class == 'Slender':
                # TODO add this as dic for optimised and ignore
                logger.warning("The trial section ({}) is Slender. Ignoring section.".format(section))
                # pass
                # if (self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[0]) or (self.sec_profile == VALUES_SEC_PROFILE_Compression_Strut[1]):  # Angles or Back to Back Angle
                #     self.effective_area = (2 * ((31.4 * self.epsilon * self.section_property.flange_thickness) *
                #                                 self.section_property.flange_thickness)) + \
                #                           (2 * ((21 * self.epsilon * self.section_property.web_thickness) * self.section_property.web_thickness))
                # elif (self.sec_profile == VALUES_SEC_PROFILE[2]) or (self.sec_profile == VALUES_SEC_PROFILE[3]):
                #     self.effective_area = (2 * 21 * self.epsilon * self.section_property.flange_thickness) * 2
            elif self.section_property.section_class == 'Semi-Compact':
                if self.sec_profile == Profile_name_2 or self.sec_profile == Profile_name_3 :
                    # @TODO
                    pass#self.effective_area = 2 * self.section_property.area  # mm2
                else:
                    self.effective_area = self.section_property.area
                print(f"effective_area{self.effective_area}")
                # print(f"self.effective_area{self.effective_area}")

            # reduction of the area based on the connection requirements (input from design preferences)
            if self.effective_area_factor < 1.0:
                self.effective_area = round(self.effective_area * self.effective_area_factor, 2)

                logger.warning(
                    "Reducing the effective sectional area as per the definition in the Design Preferences tab.")
                logger.info(
                    "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".
                    format(round((self.effective_area / self.effective_area_factor), 2), self.effective_area))
            # else:
            #     if self.section_property.section_class != 'Slender':

        elif step == 3:
            # 2.1 - Buckling curve classification and Imperfection factor
            if (self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[:3]):
                self.buckling_class = 'c'
            else:
                self.buckling_class = None
                print("section not valid")

            self.imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(buckling_class=self.buckling_class)


        elif step == 4:
            # print(f"\n data sent "
            #       f" self.material_property.fy {self.material_property.fy}"
            #       f"self.gamma_m0 {self.gamma_m0}"
            #       f"self.slenderness {self.slenderness}"
            #       f" self.imperfection_factor {self.imperfection_factor}"
            #       f"self.section_property.modulus_of_elasticity {self.section_property.modulus_of_elasticity}")

            list_cl_7_1_2_1_design_compressisive_stress = IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                self.material_property.fy, self.gamma_m0, self.slenderness, self.imperfection_factor,
                self.section_property.modulus_of_elasticity, check_type= list_result)
            # for x in list_cl_7_1_2_1_design_compressisive_stress:
            #     print(f"x {x} ")
            self.euler_buckling_stress = list_cl_7_1_2_1_design_compressisive_stress[0]
            self.nondimensional_effective_slenderness_ratio = list_cl_7_1_2_1_design_compressisive_stress[1]
            self.phi = list_cl_7_1_2_1_design_compressisive_stress[2]
            self.stress_reduction_factor = list_cl_7_1_2_1_design_compressisive_stress[3]
            self.design_compressive_stress_fr = list_cl_7_1_2_1_design_compressisive_stress[4]
            self.design_compressive_stress = list_cl_7_1_2_1_design_compressisive_stress[5]
            self.design_compressive_stress_max = list_cl_7_1_2_1_design_compressisive_stress[6]
        elif step == 5:
            # 1- Based on optimum UR
            self.optimum_section_ur_results[self.ur] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.optimum_section_ur_results[self.ur][j] = k
                    # k += 1
                    list_2.pop(0)
                    break

            # 2- Based on optimum cost
            self.optimum_section_cost_results[self.cost] = {}

            list_2 = list_result.copy()
            for j in list_1:
                for k in list_2:
                    self.optimum_section_cost_results[self.cost][j] = k
                    list_2.pop(0)
                    break
            # print(f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
            #       f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}")
        elif step == 6:

            self.single_result[self.sec_profile] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.single_result[self.sec_profile][j] = k
                    # k += 1
                    list_2.pop(0)
                    break
            print(f"\n self.single_result {self.single_result}")
        # elif step == 7:
        #     if self.section_property.thickness < 20:
        #         self.fy == self.section_property.fy_20
        #     elif self.section_property.thickness >= 20 and self.section_property.thickness < 40:
        #         self.fy = self.section_property.fy_20_40
        #     elif self.section_property.thickness >= 40:
        #         self.fy = self.section_property.fy_40
            # initial check


    def common_result(self, list_result,result_type, flag = 1):
            self.result_designation = list_result[result_type]['Designation']
            self.result_section_class = list_result[result_type]['Section class']
            self.result_effective_area = list_result[result_type]['Effective area']

            self.result_bc = list_result[result_type]['Buckling_class']
            # self.result_bc_yy = list_result[result_type]['Buckling_curve_yy']

            self.result_IF = list_result[result_type]['IF']
            # self.result_IF_yy = list_result[result_type]['IF_yy']

            self.result_eff_len = list_result[result_type]['Effective_length']
            # self.result_eff_len_yy = list_result[result_type]['Effective_length_yy']

            self.result_eff_sr = list_result[result_type]['Effective_SR']
            # self.result_eff_sr_yy = list_result[result_type]['Effective_SR_yy']
            self.result_lambda_vv = list_result[result_type]['lambda_vv']

            self.result_lambda_psi = list_result[result_type]['lambda_psi']


            self.result_ebs = list_result[result_type]['EBS']
            # self.result_ebs_yy = list_result[result_type]['EBS_yy']

            self.result_nd_esr = list_result[result_type]['ND_ESR']
#                 self.result_nd_esr_yy = list_result[result_type]['ND_ESR_yy']

            self.result_phi_zz = list_result[result_type]['phi']
#                 self.result_phi_yy = list_result[result_type]['phi_yy']

            self.result_srf = list_result[result_type]['SRF']
#                 self.result_srf_yy = list_result[result_type]['SRF_yy']

            self.result_fcd_1_zz = list_result[result_type]['FCD_formula']
#                 self.result_fcd_1_yy = list_result[result_type]['FCD_1_yy']

            self.result_fcd_2 = list_result[result_type]['FCD_max']

            # self.result_fcd_zz = list_result[result_type]['FCD_zz']
            # self.result_fcd_yy = list_result[result_type]['FCD_yy']

            self.result_fcd = list_result[result_type]['FCD'] * 1000
            self.result_capacity = list_result[result_type]['Capacity']
            self.result_cost = list_result[result_type]['Cost']
    # def max_force_length(self,section):
    #
    #     "calculated max force and length based on the maximum section size avaialble for diff section type"
    #
    #     if self.sec_profile == 'Angles':
    #         # print (Angle)
    #
    #         self.section_size_max = Angle(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         self.max_member_force = self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile,subkey=self.loc, D_a=self.section_size_max.a,
    #                                    B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #     elif self.sec_profile in ['Back to Back Angles', 'Star Angles']:
    #         self.section_size_max = Angle(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(2*self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         # self.max_member_force = self.section_size_max.tension_yielding_capacity * 2
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.a,
    #                                    B_b=self.section_size_max.b, T_t=self.section_size_max.thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #
    #
    #     elif self.sec_profile == 'Channels':
    #         self.section_size_max = Channel(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #
    #         self.max_member_force = self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile,subkey=self.loc, D_a=self.section_size_max.depth,
    #                                    B_b=self.section_size_max.flange_width, T_t=self.section_size_max.flange_thickness,
    #                                    t=self.section_size_max.web_thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #
    #
    #     elif self.sec_profile == 'Back to Back Channels':
    #         self.section_size_max = Channel(designation=section, material_grade=self.material)
    #         self.section_size_max.tension_member_yielding(A_g=(2*self.section_size_max.area),
    #                                                       F_y=self.section_size_max.fy)
    #         # self.max_member_force = 2 * self.section_size_max.tension_yielding_capacity
    #         self.min_rad_gyration_calc(self,designation=section, material_grade=self.material,
    #                                    key=self.sec_profile, subkey=self.loc, D_a=self.section_size_max.depth,
    #                                    B_b=self.section_size_max.flange_width, T_t=self.section_size_max.flange_thickness,
    #                                    t=self.section_size_max.web_thickness)
    #         self.max_length = 400 * self.min_radius_gyration
    #     self.section_size_max.design_check_for_slenderness(K=self.K, L=self.length,
    #                                                    r=self.min_radius_gyration)
    #
    #     return self.section_size_max.tension_yielding_capacity, self.max_length, self.section_size_max.slenderness,self.min_radius_gyration

    def design(self, design_dictionary , flag = 0):
        """ Perform design of struct """
        # checking DP inputs
        self.optimization_tab_check(self)

        print(f"\nSections passing initial checks {self.input_section_list}\n")
        if design_dictionary[KEY_AXIAL] == '' and len(self.input_section_list) == 1 :
            self.single_result = {}
            # logger.info("Provided appropriate input and starting design.")
            self.strength_of_strut(self)
        elif design_dictionary[KEY_AXIAL] != '' :
            if len(self.input_section_list) > 1 :
                logger.info("Provided appropriate input and starting design.")
                self.design_strut(self)
            elif len(self.input_section_list) != 0 :
                logger.warning(
                    "No need for load input.")
                # logger.error("Cannot compute!")
                logger.info(" Ignoring load and starting design.")
                design_dictionary[KEY_AXIAL] = ''
                self.strength_of_strut(self)
            else:
                # logger.warning(
                #     "More than 1 section given as input without giving Load")
                logger.warning("Cannot compute!")
                logger.info("Give 1 valid section as Inputs and/or "
                            "Change load or Length and re-design.")
                self.design_status = False
                # self.design_strut(self)
                self.design_status_list.append(self.design_status)

        else:
            # logger.warning(
            #     "More than 1 section given as input without giving Load")
            logger.warning("Cannot compute!")
            design_dictionary[KEY_AXIAL] == 1
            logger.info(" Taking load of 1 kN.")
            # logger.info("Give 1 section as Inputs and/or "
            #             "Give load and re-design.")
            # self.design_status = False
            self.design_strut(self)
            # self.design_status_list.append(self.design_status)

    def design_strut(self):

        # initializing lists to store the optimum results based on optimum UR and cost
        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []

        if self.effective_area_factor == 1.0:
            logger.info(
                "The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007].")
        for section in self.input_section_list:  # iterating the design over each section to find the most optimum section

            # Common checks
            self.common_checks_1(self, section)
            # initialize lists for updating the results dictionary
            list_result = []
            list_result.append(section)
            print(f"Common checks "
                  f"list_result {list_result}")


            self.section_property.section_class = self.input_section_classification[section]

            # MIN RADIUS OF GYRATION
            self.min_radius_gyration = self.sec_prop_initial_dict[section][1]
            self.slenderness = self.sec_prop_initial_dict[section][2]
            # Step 1 - computing the effective sectional area
            self.effective_area = self.sec_prop_initial_dict[section][3]

            self.common_checks_1(self, section, step=2)



            # if self.loc == "Long Leg":
            #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
            # else:
            #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

            list_result.extend([self.section_property.section_class, self.effective_area])

            # Step 2 - computing the design compressive stress
            self.common_checks_1(self, section, step=3)
            list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])

            if self.load_type == 'Concentric Load':
                print(f"step == 4"
                      f"list_result {list_result}")
                self.lambda_vv = 'NA'
                self.lambda_psi = 'NA'
                # step == 4
                self.common_checks_1(self, section, step=4, list_result=['Concentric'])
            else:
                # self.min_radius_gyration = min(self.section_property.rad_of_gy_y, self.section_property.rad_of_gy_z)
                returned_list = IS800_2007.cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(
                    self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                    self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy,
                    bolt_no=self.bolts, fixity=self.fixity)

                self.equivalent_slenderness = returned_list[0]
                self.lambda_vv = round(returned_list[1], 2)
                self.lambda_psi = round(returned_list[2], 2)
                self.k1 = returned_list[3]
                self.k2 = returned_list[4]
                self.k3 = returned_list[5]

                self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])


            # 2.7 - Capacity of the section
            self.section_capacity = self.design_compressive_stress * self.effective_area  # N

            print("\n data sent ", self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                  f" \n self.section_property.leg_b_length {self.section_property.leg_b_length}, ",
                  f"\n  self.section_property.thickness {self.section_property.thickness},",
                  f" \n self.material_property.fy {self.material_property.fy}, ",
                  f"\n self.bolts {self.bolts}, ",
                  f" \n self.fixity {self.fixity}, ",
                  f"\n self.slenderness {self.slenderness}",
                  f" \n self.slenderness {self.slenderness}", self.imperfection_factor,
                  self.section_property.modulus_of_elasticity,
                  f" \n self.euler_buckling_stress {self.euler_buckling_stress}",
                  f" \n self.nondimensional_effective_slenderness_ratio {self.nondimensional_effective_slenderness_ratio}",
                  f" \n self.phi {self.phi}",
                  f" \n self.stress_reduction_factor {self.stress_reduction_factor}",
                  f" \n self.design_compressive_stress_fr {self.design_compressive_stress_fr}",
                  f" \n self.design_compressive_stress {self.design_compressive_stress}",
                  f" \n self.design_compressive_stress_max {self.design_compressive_stress_max}"
                  f" \n self.section_capacity {self.section_capacity}", )
            if self.load_type != 'Concentric Load':
                print(f" \n self.equivalent_slenderness {self.equivalent_slenderness} "
                      f" \n self.lambda_vv {self.lambda_vv} "
                      f" \n self.lambda_psi {self.lambda_psi} "
                      f" \n self.k1 {self.k1} "
                      f" \n self.k2 {self.k2} "
                      f" \n self.k3 {self.k3} ")
            # 2.8 - UR
            self.ur = round(self.load.axial_force / self.section_capacity, 3)
            self.optimum_section_ur.append(self.ur)

            # 2.9 - Cost of the section in INR
            self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * self.length * \
                        self.steel_cost_per_kg
            self.optimum_section_cost.append(self.cost)

            list_result.extend([self.slenderness, self.euler_buckling_stress,
                                self.lambda_vv, self.lambda_psi,
                                self.nondimensional_effective_slenderness_ratio,
                                self.phi, self.stress_reduction_factor,
                                self.design_compressive_stress_fr,
                                self.design_compressive_stress_max,
                                self.design_compressive_stress,
                                self.section_capacity, self.ur, self.cost]
                               )
            print("Section result: \n",self.sec_profile, list_result)
            # Step 3 - Storing the optimum results to a list in a descending order

            list_1 = ['Designation','Section class', 'Effective area', 'Buckling_class', 'IF',
                      'Effective_length', 'Effective_SR', 'EBS', 'lambda_vv', 'lambda_psi', 'ND_ESR', 'phi', 'SRF',
                      'FCD_formula', 'FCD_max', 'FCD', 'Capacity', 'UR', 'Cost']
            self.common_checks_1(self, section, 5, list_result, list_1)
            print(f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
              f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}")
            
    def design_check_for_slenderness(self, K, L, r):
        "KL= effective length of member"
        "r = radius of gyration of member"
        slender = (float(K) * float(L)) / float(r)
        self.slenderness = round(slender, 2)
        return self.slenderness
    
    def min_rad_gyration_calc_strut(self,designation, material_grade,key,subkey, D_a=0.0,B_b=0.0,T_t=0.0,t=0.0):
        if key == Profile_name_1 and (subkey == loc_type1 or subkey == loc_type2):
            self.Angle_attributes = Angle(designation, material_grade)
            effective_area = self.Angle_attributes.area
            rad_u = self.Angle_attributes.rad_of_gy_u
            rad_v = self.Angle_attributes.rad_of_gy_v
            min_rad = min(rad_u, rad_v)

        elif key == Profile_name_2 and subkey == loc_type1:
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t,l=loc_type2, thickness = 0) * 10
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t,l=loc_type2, thickness = 0) * 10
            # mom_inertia_y_1 = mom_inertia_y = self.self.Angle_attributes.mom_inertia_y
            # mom_inertia_z_1 = mom_inertia_y = self.Angle_attributes.mom_inertia_y
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=T_t, l=loc_type2, thickness = 0)
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=T_t, l=loc_type2, thickness = 0)
            print(self.section_property.designation, '\n rad_y =',rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',mom_inertia_y,'\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_2 and subkey == loc_type2: #match
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=T_t, l=loc_type1, thickness= 0)
            print(self.section_property.designation, '\n rad_y =',rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',mom_inertia_y,'\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_3 and subkey == loc_type1: #match
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            print(self.section_property.designation, '\n rad_y =', rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',
                  mom_inertia_y, '\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        elif key == Profile_name_3 and subkey == loc_type2:
            BBAngle_attributes = BBAngle_Properties()
            BBAngle_attributes.data(designation, material_grade)
            effective_area = BBAngle_attributes.calc_Area() * 100
            rad_y = BBAngle_attributes.calc_RogY(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_y = BBAngle_attributes.calc_MomentOfAreaY(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            rad_z = BBAngle_attributes.calc_RogZ(a=D_a,b=B_b,t=T_t, l=subkey, thickness= t) * 10
            mom_inertia_z = BBAngle_attributes.calc_MomentOfAreaZ(a=D_a,b=B_b,t=0, l=loc_type1, thickness= t)
            print(self.section_property.designation, '\n rad_y =', rad_y, '\n rad_z =', rad_z, '\n mom_inertia_y =',
                  mom_inertia_y, '\n mom_inertia_z', mom_inertia_z)
            min_rad = min(rad_y, rad_z)
        return min_rad , effective_area
    
    def strength_of_strut(self, load = None, len = 1):
        # iterating the design over each section to find the most optimum section
        section = self.input_section_list[0]
        self.single_result = {}
        # Yield strength of steel
        # self.common_checks_1(self,section, step=7)
        # Common checks
        self.common_checks_1(self, section)
        # initialize lists for updating the results dictionary
        list_result = []
        list_result.append(section)
        print(f"Common checks "
              f"section for design {list_result}")

        # Step 1 - section class
        self.section_property.section_class = self.input_section_classification[section]

        # MIN RADIUS OF GYRATION
        self.min_radius_gyration = self.sec_prop_initial_dict[section][1]
        self.slenderness = self.sec_prop_initial_dict[section][2]
        
        # Step 1 - computing the effective sectional area
        self.effective_area = self.sec_prop_initial_dict[section][3]
        # SAME AS BEFORE

        self.common_checks_1(self, section, step=2)
        # if self.loc == "Long Leg":
        #     self.max_depth =self.section_size_max.max_leg - self.section_size_max.thickness - self.section_size_max.root_radius
        # else:
        #     self.max_depth =self.section_size_max.min_leg - self.section_size_max.thickness - self.section_size_max.root_radius

        list_result.extend([self.section_property.section_class, self.effective_area])

        # Step 2 - computing the design compressive stress
        self.common_checks_1(self, section, step=3)
        list_result.extend([self.buckling_class, self.imperfection_factor, self.effective_length])

        if self.load_type == 'Concentric Load':
            # print(f"step == 4"
            #       f"list_result {list_result}")
            self.lambda_vv = 'NA'
            self.lambda_psi = 'NA'
            # step == 4
            self.common_checks_1(self, section, step=4, list_result=['Concentric'])
        else:
            # self.min_radius_gyration = min(self.section_property.rad_of_gy_y, self.section_property.rad_of_gy_z)
            returned_list = IS800_2007.cl_7_5_1_2_equivalent_slenderness_ratio_of_truss_compression_members_loaded_one_leg(
                self.length, self.min_radius_gyration, self.section_property.leg_a_length,
                self.section_property.leg_b_length, self.section_property.thickness, self.material_property.fy,
                bolt_no=self.bolts, fixity=self.fixity)

            self.equivalent_slenderness = returned_list[0]
            self.lambda_vv = round(returned_list[1], 2)
            self.lambda_psi = round(returned_list[2], 2)
            self.k1 = returned_list[3]
            self.k2 = returned_list[4]
            self.k3 = returned_list[5]


            self.common_checks_1(self, section, step=4, list_result=['Leg', self.equivalent_slenderness])

        print("\n data sent ", self.length, self.min_radius_gyration, self.section_property.leg_a_length,
              f" \n self.section_property.leg_b_length {self.section_property.leg_b_length}, ",
              f"\n  self.section_property.thickness {self.section_property.thickness},",
              f" \n self.material_property.fy {self.material_property.fy}, ",
               f"\n self.bolts {self.bolts}, ",
              f" \n self.fixity {self.fixity}, ",
               f"\n self.slenderness {self.slenderness}",
              f" \n self.imperfection_factor {self.imperfection_factor}", self.section_property.modulus_of_elasticity,
              f" \n self.euler_buckling_stress {self.euler_buckling_stress}",
              f" \n self.nondimensional_effective_slenderness_ratio {self.nondimensional_effective_slenderness_ratio}",
              f" \n self.phi {self.phi}",
              f" \n self.stress_reduction_factor {self.stress_reduction_factor}",
              f" \n self.design_compressive_stress_fr {self.design_compressive_stress_fr}",
              f" \n self.design_compressive_stress {self.design_compressive_stress}",
              f" \n self.design_compressive_stress_max {self.design_compressive_stress_max}", )
        if self.load_type != 'Concentric Load':
                  print(f" \n self.equivalent_slenderness {self.equivalent_slenderness} "
                  f" \n self.lambda_vv {self.lambda_vv} "
                  f" \n self.lambda_psi {self.lambda_psi} "
                  f" \n self.k1 {self.k1} "
                  f" \n self.k2 {self.k2} "
                  f" \n self.k3 {self.k3} ")
        # 2.7 - Capacity of the section
        self.section_capacity = self.design_compressive_stress * self.effective_area  # N

        #SAME AS BEFORE TILL HERE

        # 2.9 - Cost of the section in INR
        self.cost = (self.section_property.unit_mass * self.section_property.area * 1e-4) * self.length * \
                    self.steel_cost_per_kg
        self.ur = load/self.load if load is not None else "NA"
        list_result.extend([self.slenderness, self.euler_buckling_stress,
                                self.lambda_vv, self.lambda_psi,
                                self.nondimensional_effective_slenderness_ratio,
                                self.phi, self.stress_reduction_factor,
                                self.design_compressive_stress_fr,
                                self.design_compressive_stress_max,
                                self.design_compressive_stress,
                                self.section_capacity,self.ur, self.cost]
                           )
        print(f"list_result {list_result}")
        # Step 3 - Storing the optimum results to a list in a descending order

        list_1 = ['Designation', 'Section class', 'Effective area', 'Buckling_class', 'IF',
                  'Effective_length', 'Effective_SR', 'EBS', 'lambda_vv', 'lambda_psi', 'ND_ESR', 'phi', 'SRF',
                  'FCD_formula', 'FCD_max', 'FCD', 'Capacity', 'UR', 'Cost']

        self.common_checks_1(self, section, step = 6, list_result= list_result, list_1= list_1)
        #     break

    def results(self,design_dictionary):
        """ """
        # sorting results from the dataset
        if len(self.input_section_list) > 1 :
            if design_dictionary[KEY_AXIAL] != '':
                # results based on UR
                if self.optimization_parameter == 'Utilization Ratio':
                    filter_UR = filter(lambda x: x <= min(self.allowable_utilization_ratio, 1.0), self.optimum_section_ur)
                    self.optimum_section_ur = list(filter_UR)

                    self.optimum_section_ur.sort()
                    # print(f"self.optimum_section_ur{self.optimum_section_ur}")
                    #print(f"self.result_UR{self.result_UR}")

                    # selecting the section with most optimum UR
                    if len(self.optimum_section_ur) == 0:  # no design was successful
                        logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                        "criteria")
                        logger.error("The solver did not find any adequate section from the defined list.")
                        logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                        self.design_status = False
                        self.design_status_list.append(self.design_status)

                    else:
                        self.result_UR = self.optimum_section_ur[-1]  # optimum section which passes the UR check
                        print(f"self.result_UR{self.result_UR}")
                        self.design_status = True

                else:  # results based on cost
                    self.optimum_section_cost.sort()

                    # selecting the section with most optimum cost
                    self.result_cost = self.optimum_section_cost[0]

                # print results
                if len(self.optimum_section_ur) == 0:
                    logger.warning(
                        "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                        "criteria")
                    logger.error("The solver did not find any adequate section from the defined list.")
                    logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                    self.design_status = False
                    self.design_status_list.append(self.design_status)
                    pass
                else:
                    if self.optimization_parameter == 'Utilization Ratio':
                        print(f" self.optimum_section_ur_results {self.optimum_section_ur_results}")
                        self.common_result(self, list_result=self.optimum_section_ur_results, result_type=self.result_UR)
                    else:
                        self.result_UR = self.optimum_section_cost_results[self.result_cost]['UR']

                        # checking if the selected section based on cost satisfies the UR
                        if self.result_UR > min(self.allowable_utilization_ratio, 1.0):

                            trial_cost = []
                            for cost in self.optimum_section_cost:
                                self.result_UR = self.optimum_section_cost_results[cost]['UR']
                                if self.result_UR <= min(self.allowable_utilization_ratio, 1.0):
                                    trial_cost.append(cost)

                            trial_cost.sort()

                            if len(trial_cost) == 0:  # no design was successful
                                logger.warning("The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                                                "criteria")
                                logger.error("The solver did not find any adequate section from the defined list.")
                                logger.info("Re-define the list of sections or check the Design Preferences option and re-design.")
                                self.design_status = False
                                self.design_status_list.append(self.design_status)
                                print(f"design_status_list{self.design_status} \n")
                            else:
                                self.result_cost = trial_cost[0]  # optimum section based on cost which passes the UR check
                                self.design_status = True

                        # results
                        self.common_result(self, list_result=self.optimum_section_cost_results, result_type=self.result_cost)

                        print(f"design_status_list2{self.design_status}")
                for status in self.design_status_list:
                    if status is False:
                        self.design_status = False
                        break
                    else:
                        self.design_status = True
            else:
                logger.warning(
                    "More than 1 section given as input without giving Load")
                logger.error("Cannot compute!")
                logger.info("Give 1 section as Inputs and/or "
                            "Give load and re-design.")
                self.design_status = False
                self.design_status_list.append(self.design_status)
            if self.design_status:
                logger.info(": ========== Design Status ============")
                logger.info(": Overall Column design is SAFE")
                logger.info(": ========== End Of Design ============")
            else:
                logger.info(": ========== Design Status ============")
                logger.info(": Overall Column design is UNSAFE")
                logger.info(": ========== End Of Design ============")
        else:

            print(f"self.single_result {self.single_result}"
                  )
            self.common_result(self, list_result=self.single_result,result_type= self.sec_profile, flag= 1)
            self.design_status = True
            self.result_UR = self.single_result[self.sec_profile]['UR']
            if self.design_status:
                logger.info(": ========== Capacity Status ============")
                logger.info(": Section satisfies input")
                logger.info(": Section strength found")
                logger.info(": ========== End Of Status ============")
            else:
                logger.info(": ========== Capacity Status ============")
                logger.info(": Section does not satisfies input")
                logger.info(": Section strength NOT found")
                logger.info(": ========== End Of Status ============")
        # end of the design simulation
        # overall design status




    ### start writing save_design from here!
    def save_design(self, popup_summary):
        self.failed_design_dict = None
        if (self.design_status and self.failed_design_dict is None) or (not self.design_status and len(self.failed_design_dict)>0):# TODO @Rutvik
            self.section_property = self.section_connect_database(self, self.result_designation)
            if self.sec_profile in VALUES_SEC_PROFILE_Compression_Strut[2]:
                # connecting_plates = [self.plate.thickness_provided, section_size.web_thickness]
                if self.section_property.max_leg == self.section_property.min_leg:
                    if self.loc == "Long Leg":
                        image = "bblequaldp"
                    else:
                        image = "bbsequaldp"
                else:
                    if self.loc == "Long Leg":
                        image = "bblunequaldp"
                    else:
                        image = "bbsunequaldp"
            else:
                    image = "broken"
            # min_gauge = self.pitch_round
            # row_limit = "Row~Limit~(rl)~=~2"
            # row = 2
            # depth =  2 * self.edge_dist_min_round + self.pitch_round
            if self.section_property=='Columns' or self.section_property=='Beams':
                self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
                                        KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                        KEY_DISP_MATERIAL: self.section_property.material,
        #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                        KEY_REPORT_MASS: self.section_property.mass,
                                        KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                        KEY_REPORT_DEPTH: self.section_property.depth,
                                        KEY_REPORT_WIDTH: self.section_property.flange_width,
                                        KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                        KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                        KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope,
                                        KEY_REPORT_R1: self.section_property.root_radius,
                                        KEY_REPORT_R2: self.section_property.toe_radius,
                                        KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
                                        KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
                                        KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
                                        KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
                                        KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
                                        KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
                                        KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
                                        KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}
            elif self.sec_profile == "Angles":
                self.report_column = {KEY_DISP_SEC_PROFILE: image,
                                        # Image shall be save with this name.png in resource files
                                        KEY_DISP_SECSIZE: (self.section_property.designation,self.sec_profile),
                                        KEY_DISP_MATERIAL: self.section_property.material,
                                        KEY_REPORT_MASS: round(self.section_property.mass,2),
                                        KEY_REPORT_AREA: round(self.section_property.area,2),
                                        KEY_REPORT_MAX_LEG_SIZE: round(self.section_property.max_leg,2),
                                        KEY_REPORT_MIN_LEG_SIZE: round(self.section_property.min_leg,2),
                                        KEY_REPORT_ANGLE_THK: round(self.section_property.thickness,2),
                                        KEY_REPORT_R1: round(self.section_property.root_radius,2),
                                        KEY_REPORT_R2: round(self.section_property.toe_radius,2),
                                        KEY_REPORT_CY: round(self.section_property.Cy,2),
                                        KEY_REPORT_CZ: round(self.section_property.Cz,2),
                                        KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4,2),
                                        KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4,2),
                                        KEY_REPORT_IU: round(self.section_property.mom_inertia_u * 1e-4,2),
                                        KEY_REPORT_IV: round(self.section_property.mom_inertia_v * 1e-4,2),
                                        KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1,2),
                                        KEY_REPORT_RY: round((self.section_property.rad_of_gy_y) * 1e-1,2),
                                        KEY_REPORT_RU: round((self.section_property.rad_of_gy_u) * 1e-1,2),
                                        KEY_REPORT_RV: round((self.section_property.rad_of_gy_v) * 1e-1,2),
                                        KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3,2),
                                        KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3,2),
                                        KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3,2),
                                        KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3,2),
                                        # KEY_REPORT_RADIUS_GYRATION: round(gyration,2)
                                        }
            else:
                self.report_column = {KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                        KEY_DISP_MATERIAL: self.section_property.material,
                                        #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                        KEY_REPORT_MASS: self.section_property.mass,
                                        KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                        KEY_REPORT_DEPTH: self.section_property.depth,
                                        KEY_REPORT_WIDTH: self.section_property.flange_width,
                                        KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                        KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                        KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope}


        self.report_input = \
            {KEY_MAIN_MODULE: self.mainmodule,
                KEY_MODULE: self.module, #"Axial load on column "
                KEY_DISP_SECTION_PROFILE: self.sec_profile,
                KEY_MATERIAL: self.material,
                KEY_DISP_LENGTH_BEAM: self.length,
                KEY_DISP_SECSIZE: str(self.sec_list),
                # KEY_DISP_ACTUAL_LEN_YY: self.length_yy,
                KEY_DISP_END1: self.end_1,
                KEY_DISP_END2: self.end_2,
                KEY_DISP_AXIAL: self.load.axial_force,
                KEY_DISP_SEC_PROFILE: self.sec_profile,
                KEY_DISP_SECSIZE: self.result_section_class,
                # KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.euler_bs_yy,
                # KEY_DISP_YIELD_STRENGTH_REPORT: self.result_bc_yy,
                "Column Section - Mechanical Properties": "TITLE",
                "Selected Section Details": self.report_column,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                "Design Preference" : "TITLE"
        #         KEY_DISP_UR : self.allowable_utilization_ratio,
        #         KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
        #         KEY_DISP_CLASS: self.allow_class,
        #         Buckling_Out_plane: ,
        #         Buckling_In_plane: ,
        #         KEY_DISP_LOAD: self.load_type,
        #         Strut_Bolt_Number: ,
                
                }
        # if self.sec_profile == Profile_name_2:
        #     self.report_input.update({
        #         'Gusset '+ KEY_GUSSET: ,
                
        #     })
        self.report_check = []

        # self.h = (self.beam_D - (2 * self.beam_tf))

        #1.1 Input sections display
        # t1 = ('SubSection', 'List of Input Sections',self.input_section_list)
        t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
        self.report_check.append(t1)
        
        t1 = ('SubSection', 'Trial', '|p{4cm}|p{1.5cm}|p{9.5cm}|p{1cm}|')
        self.report_check.append(t1)
        t1 = ("h/bf , tf ", 'comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf)',
                'comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf)',
                'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        self.report_check.append(t1)
        
        # 2.2 CHECK: Buckling Class - Compatibility Check
        # t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        # self.report_check.append(t1)

        # t1 = ("h/bf , tf ", 'comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf)',
        #         'comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf)',
        #         'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)

        # 2.3 CHECK: Cross-section classification
        # t1 = ('SubSection', 'Cross-section classification', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        # self.report_check.append(t1)

        # t1 = ("b/tf and d/tw ", cross_section_classification_required(self.section),
        #         cross_section_classification_provided(self.tf, self.b1, self.epsilon, self.section, self.b1_tf,
        #                                             self.d1_tw, self.ep1, self.ep2, self.ep3, self.ep4),
        #         'b = bf / 2,d = h – 2 ( T + R1),έ = (250 / Fy )^0.5,Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)

        # # 2.4 CHECK : Member Check
        # t1 = ("Slenderness", cl_7_2_2_slenderness_required(self.KL, self.ry, self.lamba),
        #         cl_7_2_2_slenderness_provided(self.KL, self.ry, self.lamba), 'PASS')
        # self.report_check.append(t1)

        # t1 = (
        # "Design Compressive stress (fcd)", cl_7_1_2_1_fcd_check_required(self.gamma_mo, self.f_y, self.f_y_gamma_mo),
        # cl_7_1_2_1_fcd_check_provided(self.facd), 'PASS')
        # self.report_check.append(t1)

        # t1 = ("Design Compressive strength (Pd)", cl_7_1_2_design_comp_strength_required(self.axial),
        #         cl_7_1_2_design_comp_strength_provided(self.Aeff, self.facd, self.A_eff_facd), "PASS")
        # self.report_check.append(t1)

        # t1 = ('', '', '', '')
        # self.report_check.append(t1)
        # print(sys.path[0])
        # rel_path = str(sys.path[0])
        # rel_path = rel_path.replace("\\", "/")
        # fname_no_ext = popup_summary['filename']
        # CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
        #                         rel_path, module=self.module)
        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        print('self.report_input:',self.report_input)
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                              rel_path, [], '', module=self.module) 
    # def memb_pattern(self, status):
    #
    #     if self.sec_profile in ['Angles', 'Back to Back Angles', 'Star Angles']:
    #         image = './ResourceFiles/images/L.png'
    #         x, y = 400, 202
    #
    #     else:
    #         image = './ResourceFiles/images/U.png'
    #         x, y = 400, 202
    #
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Member', TYPE_IMAGE,
    #            [image, x, y, "Member Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern
    #
    # def plate_pattern(self, status):
    #
    #     pattern = []
    #
    #     t00 = (None, "", TYPE_NOTE, "Representative image for Failure Pattern - 2 x 3 Bolts pattern considered")
    #     pattern.append(t00)
    #
    #     t99 = (None, 'Failure Pattern due to Tension in Plate', TYPE_IMAGE,
    #            ['./ResourceFiles/images/L.png',400,202, "Plate Block Shear Pattern"])  # [image, width, height, caption]
    #     pattern.append(t99)
    #
    #     return pattern