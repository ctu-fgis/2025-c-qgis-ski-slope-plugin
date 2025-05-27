"""
Model exported as python.
Name : modelVec
Group : 
With QGIS : 33412
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelvec(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('budovy', 'Budovy', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('chranenna_uzemi', 'Chranenna uzemi', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('silnice', 'Silnice', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('sjezd', 'Sjezd', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('vodnitoky', 'Vodnitoky', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('zeleznice', 'Zeleznice', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Vyselektovaneuzemi', 'Vyselektovaneuzemi', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        # Obalová zóna Z
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 60,
            'END_CAP_STYLE': 0,  # Kulatý
            'INPUT': parameters['zeleznice'],
            'JOIN_STYLE': 0,  # Kulatý
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ObalovZnaZ'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Obalová zóna S
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 100,
            'END_CAP_STYLE': 0,  # Kulatý
            'INPUT': parameters['silnice'],
            'JOIN_STYLE': 0,  # Kulatý
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ObalovZnaS'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Obalová zóna B
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 30,
            'END_CAP_STYLE': 0,  # Kulatý
            'INPUT': parameters['budovy'],
            'JOIN_STYLE': 0,  # Kulatý
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ObalovZnaB'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Obalová zóna VT
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 50,
            'END_CAP_STYLE': 0,  # Kulatý
            'INPUT': parameters['vodnitoky'],
            'JOIN_STYLE': 0,  # Kulatý
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ObalovZnaVt'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Rozdíl VT
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': parameters['sjezd'],
            'OVERLAY': outputs['ObalovZnaVt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RozdlVt'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Rozdíl S
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RozdlVt']['OUTPUT'],
            'OVERLAY': outputs['ObalovZnaS']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RozdlS'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Rozdíl Z
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RozdlS']['OUTPUT'],
            'OVERLAY': outputs['ObalovZnaZ']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RozdlZ'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Rozdíl B
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RozdlZ']['OUTPUT'],
            'OVERLAY': outputs['ObalovZnaB']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RozdlB'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Rozdíl CH
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RozdlB']['OUTPUT'],
            'OVERLAY': parameters['chranenna_uzemi'],
            'OUTPUT': parameters['Vyselektovaneuzemi']
        }
        outputs['RozdlCh'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Vyselektovaneuzemi'] = outputs['RozdlCh']['OUTPUT']
        return results

    def name(self):
        return 'modelVec'

    def displayName(self):
        return 'modelVec'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelvec()
