# Python Imports
import sys
import argparse
import unittest
from unittest.mock import Mock, patch

# Third-Party Imports

# Project Imports
from frag_pele.Helpers import argument_parser as ap
import frag_pele.constants as const


class TestArgumentParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.class_parser = argparse.ArgumentParser()

    @patch.object(ap, '_add_all_arguments')
    def test_create_parser(self, mock_argparser_lib):
        parser = ap._create_parser()

        mock_argparser_lib.assert_called_once_with(parser)
        self.assertEqual(type(parser), argparse.ArgumentParser)

    @patch.object(ap, "_add_frag_required_named_arguments")
    @patch.object(ap, "_add_frag_standard_arguments")
    @patch.object(ap, "_add_plop_arguments")
    @patch.object(ap, "_add_pele_conf_arguments")
    @patch.object(ap, "_add_clustering_arguments")
    @patch.object(ap, "_add_protocol_arguments")
    @patch.object(ap, "_add_output_format_arguments")
    @patch.object(ap, "_add_others_arguments")
    def test_add_all_arguments(self, mock_a, mock_b, mock_c, mock_d, mock_e, mock_f, mock_g, mock_h):
        parser = argparse.ArgumentParser()

        ap._add_all_arguments(parser)
        mock_a.assert_called_once_with(parser)
        mock_b.assert_called_once_with(parser)
        mock_c.assert_called_once_with(parser)
        mock_d.assert_called_once_with(parser)
        mock_e.assert_called_once_with(parser)
        mock_f.assert_called_once_with(parser)
        mock_g.assert_called_once_with(parser)
        mock_h.assert_called_once_with(parser)

    def test_add_required_named_arguments(self):
        flags_to_check = ['-cp', '--complex_pdb', '-sef', '--serie_file']

        parser = argparse.ArgumentParser()
        ap._add_frag_required_named_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(6, len(actions))  # 6 and not 4 as in flag_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_standard_arguments(self):
        flags_to_check = ['--core', '-nc', '--no_check', '-x', '--growing_steps', '-cr', '--criteria', '-rst',
                          '--restart', '-cc', '--c_chain', '-fc', '--f_chain', '-tc', '--clash_thr', '-sc',
                          '--sampling_control', '-op', '--only_prepare', '-og', '--only_grow']

        parser = argparse.ArgumentParser()
        ap._add_frag_standard_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(23, len(actions))  # 23 and not 21 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_plop_arguments(self):
        flags_to_check = ['-pl', '--plop_path', '-sp', '--sch_python', '-rot', '--rotamers']

        parser = argparse.ArgumentParser()
        ap._add_plop_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(8, len(actions))  # 8 and not 6 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_pele_conf_arguments(self):
        flags_to_check = ['-d', '--pele_dir', '-c', '--contrl', '-l', '--license', '-r', '--resfold', '-rp', '--report',
                          '-tj', '--traject', '-cs', '--cpus', '-stp', '--steps', '-es', '--pele_eq_steps', '-miov',
                          '--min_overlap', '-maov', '--max_overlap', '-tmp', '--temperature', '-sd', '--seed', '-st',
                          '--steering', '-trh', '--translation_high', '-roth', '--rotation_high', '-trl',
                          '--translation_low', '-rotl', '--rotation_low', '-rad', '--radius_box', '-dat', '--data',
                          '-doc', '--documents']

        parser = argparse.ArgumentParser()
        ap._add_pele_conf_arguments(parser)
        actions = parser._option_string_actions
        self.assertEqual(44, len(actions))  # 44 and not 42 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_clustering_arguments(self):
        flags_to_check = ['-dis', '--distcont', '-ct', '--threshold', '-e', '--epsilon', '-cn', '--condition', '-mw',
                          '--metricweights', '-ncl', '--nclusters', '-pdbf', '--pdbout', '-ban', '--banned', '-lim',
                          '--limit']

        parser = argparse.ArgumentParser()
        ap._add_clustering_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(20, len(actions))  # 20 and not 18 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_protocol_arguments(self):
        flags_to_check = ['-HT', '--highthroughput', '-EX', '--explorative', '--test']

        parser = argparse.ArgumentParser()
        ap._add_protocol_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(7, len(actions))  # 7 and not 5 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_output_format_arguments(self):
        flags_to_check = ['--mae']

        parser = argparse.ArgumentParser()
        ap._add_output_format_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(3, len(actions))  # 3 and not 1 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_add_other_arguments(self):
        flags_to_check = ['--rename']

        parser = argparse.ArgumentParser()
        ap._add_others_arguments(parser)
        actions = parser._option_string_actions

        self.assertEqual(3, len(actions))  # 3 and not 1 as in flags_to_check, because automatically adds -h --help
        self._loop_assert_in(flags_to_check, actions)

    def test_check_highthroughput_in_args_true(self):
        mock = Mock()
        mock.highthroughput = True
        mock.growing_steps = 0
        mock.steps = 0
        mock.pele_eq_steps = 0

        ap._check_highthroughput_in_args(mock)

        self.assertEqual(mock.growing_steps, 1)
        self.assertEqual(mock.steps, 3)
        self.assertEqual(mock.pele_eq_steps, 10)

    def test_check_highthroughput_in_args_false(self):
        mock = Mock()
        mock.highthroughput = False
        mock.growing_steps = 0
        mock.steps = 0
        mock.pele_eq_steps = 0

        ap._check_highthroughput_in_args(mock)

        self.assertEqual(mock.growing_steps, 0)
        self.assertEqual(mock.steps, 0)
        self.assertEqual(mock.pele_eq_steps, 0)

    def test_check_test_in_args_true(self):
        mock = Mock()
        mock.test = True
        mock.growing_steps = 0
        mock.steps = 0
        mock.pele_eq_steps = 0
        mock.temp = 0

        ap._check_test_in_args(mock)

        self.assertEqual(mock.growing_steps, 1)
        self.assertEqual(mock.steps, 1)
        self.assertEqual(mock.pele_eq_steps, 1)
        self.assertEqual(mock.temperature, 1000000)

    def test_check_test_in_args_false(self):
        mock = Mock()
        mock.test = False
        mock.growing_steps = 0
        mock.steps = 0
        mock.pele_eq_steps = 0
        mock.temp = 0

        ap._check_test_in_args(mock)

        self.assertEqual(mock.growing_steps, 0)
        self.assertEqual(mock.steps, 0)
        self.assertEqual(mock.pele_eq_steps, 0)
        self.assertEqual(mock.temp, 0)

    def test_parse_arguments(self):
        test_args = ['TestFragArgParser', '-cp', 'TEST_CP', '-sef', 'TEST_SEF', '-nc', '-rst', '-op', '-og',
                     '-EX', '--mae', '--rename']

        expected = ['TEST_CP', 'TEST_SEF', True, 10, const.SELECTION_CRITERIA, True, 'L', 'L', 1.7, None, True, True,
                    const.PLOP_PATH, const.SCHRODINGER_PY_PATH, const.ROTRES, const.PATH_TO_PELE,
                    const.CONTROL_TEMPLATE, const.PATH_TO_LICENSE, const.RESULTS_FOLDER, const.REPORT_NAME,
                    const.TRAJECTORY_NAME, const.CPUS, const.STEPS, const.PELE_EQ_STEPS, const.MIN_OVERLAP,
                    const.MAX_OVERLAP, const.TEMPERATURE, const.SEED, const.STEERING, const.TRANSLATION_HIGH,
                    const.ROTATION_HIGH, const.TRANSLATION_LOW, const.ROTATION_LOW, const.RADIUS_BOX,
                    const.PATH_TO_PELE_DATA, const.PATH_TO_PELE_DOCUMENTS, const.DISTANCE_COUNTER,
                    const.CONTACT_THRESHOLD, const.EPSILON, const.CONDITION, const.METRICS_WEIGHTS, const.NUM_CLUSTERS,
                    const.PDBS_OUTPUT_FOLDER, const.BANNED_ANGLE_THRESHOLD, const.BANNED_DIHEDRALS_ATOMS,
                    True, True, True]

        with patch.object(sys, 'argv', test_args):
            result = ap.parse_arguments()
            self.assertEqual(len(expected), len(result))
            for i in range(len(expected)):
                self.assertEqual(expected[i], result[i])

    def test_parse_arguments_highthroughput_flag(self):
        test_args = ['TestFragArgParser', '-cp', 'TEST_CP', '-sef', 'TEST_SEF', '-nc', '-rst', '-op', '-og',
                     '-EX', '--mae', '--rename', '-HT']

        expected = ['TEST_CP', 'TEST_SEF', True, 1, const.SELECTION_CRITERIA, True, 'L', 'L', 1.7, None, True, True,
                    const.PLOP_PATH, const.SCHRODINGER_PY_PATH, const.ROTRES, const.PATH_TO_PELE,
                    const.CONTROL_TEMPLATE, const.PATH_TO_LICENSE, const.RESULTS_FOLDER, const.REPORT_NAME,
                    const.TRAJECTORY_NAME, const.CPUS, 3, 10, const.MIN_OVERLAP,
                    const.MAX_OVERLAP, const.TEMPERATURE, const.SEED, const.STEERING, const.TRANSLATION_HIGH,
                    const.ROTATION_HIGH, const.TRANSLATION_LOW, const.ROTATION_LOW, const.RADIUS_BOX,
                    const.PATH_TO_PELE_DATA, const.PATH_TO_PELE_DOCUMENTS, const.DISTANCE_COUNTER,
                    const.CONTACT_THRESHOLD, const.EPSILON, const.CONDITION, const.METRICS_WEIGHTS, const.NUM_CLUSTERS,
                    const.PDBS_OUTPUT_FOLDER, const.BANNED_ANGLE_THRESHOLD, const.BANNED_DIHEDRALS_ATOMS,
                    True, True, True]

        with patch.object(sys, 'argv', test_args):
            result = ap.parse_arguments()
            self.assertEqual(len(expected), len(result))
            for i in range(len(expected)):
                self.assertEqual(expected[i], result[i])

    def test_parse_arguments_test_flag(self):
        test_args = ['TestFragArgParser', '-cp', 'TEST_CP', '-sef', 'TEST_SEF', '-nc', '-rst', '-op', '-og',
                     '-EX', '--mae', '--rename', '--test']

        expected = ['TEST_CP', 'TEST_SEF', True, 1, const.SELECTION_CRITERIA, True, 'L', 'L', 1.7, None, True, True,
                    const.PLOP_PATH, const.SCHRODINGER_PY_PATH, const.ROTRES, const.PATH_TO_PELE,
                    const.CONTROL_TEMPLATE, const.PATH_TO_LICENSE, const.RESULTS_FOLDER, const.REPORT_NAME,
                    const.TRAJECTORY_NAME, const.CPUS, 1, 1, const.MIN_OVERLAP,
                    const.MAX_OVERLAP, 1000000, const.SEED, const.STEERING, const.TRANSLATION_HIGH,
                    const.ROTATION_HIGH, const.TRANSLATION_LOW, const.ROTATION_LOW, const.RADIUS_BOX,
                    const.PATH_TO_PELE_DATA, const.PATH_TO_PELE_DOCUMENTS, const.DISTANCE_COUNTER,
                    const.CONTACT_THRESHOLD, const.EPSILON, const.CONDITION, const.METRICS_WEIGHTS, const.NUM_CLUSTERS,
                    const.PDBS_OUTPUT_FOLDER, const.BANNED_ANGLE_THRESHOLD, const.BANNED_DIHEDRALS_ATOMS,
                    True, True, True]

        with patch.object(sys, 'argv', test_args):
            result = ap.parse_arguments()
            self.assertEqual(len(expected), len(result))
            for i in range(len(expected)):
                self.assertEqual(expected[i], result[i])

    def _loop_assert_in(self, flag_list, actions):
        for flag in flag_list:
            self.assertIn(flag, actions)
