"""
Model exported as python.
Name : model_komplet
Group : 
With QGIS : 33412
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterPointCloudLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model_komplet(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterPointCloudLayer('laz', 'LAZ', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('silnice', 'Silnice', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('budovy', 'Budovy', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('zeleznice', 'Zeleznice', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('chranenna_uzemi', 'Chranenna uzemi', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('vodnitoky', 'Vodnitoky', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Vyselektovaneuzemi', 'Vyselektovaneuzemi', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('Vysledekrastru', 'Vysledekrastru', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(17, model_feedback)
        results = {}
        outputs = {}

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

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Export to raster
        alg_params = {
            'ATTRIBUTE': 'Z',
            'FILTER_EXPRESSION': '',
            'FILTER_EXTENT': None,
            'INPUT': parameters['laz'],
            'ORIGIN_X': None,
            'ORIGIN_Y': None,
            'RESOLUTION': 1,
            'TILE_SIZE': 1000,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExportToRaster'] = processing.run('pdal:exportraster', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
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

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # r.fill.stats
        alg_params = {
            '-k': False,
            '-m': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'cells': 20,
            'distance': 20,
            'input': outputs['ExportToRaster']['OUTPUT'],
            'maximum': None,
            'minimum': None,
            'mode': 0,  # wmean
            'power': 2,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Rfillstats'] = processing.run('grass7:r.fill.stats', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
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

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

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

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Sklon
        alg_params = {
            'AS_PERCENT': False,
            'BAND': 1,
            'COMPUTE_EDGES': False,
            'EXTRA': '',
            'INPUT': outputs['Rfillstats']['output'],
            'OPTIONS': '',
            'SCALE': 1,
            'ZEVENBERGEN': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Sklon'] = processing.run('gdal:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Rastrový kalkulátor
        alg_params = {
            'CELL_SIZE': None,
            'CRS': 'ProjectCrs',
            'EXPRESSION': '"A@1">15  AND "A@1"<45',
            'EXTENT': None,
            'LAYERS': outputs['Sklon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RastrovKalkultor'] = processing.run('native:modelerrastercalc', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Pøevést na polygony (rastr na vektor)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RastrovKalkultor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PevstNaPolygonyRastrNaVektor'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Extrahovat podle výrazu
        alg_params = {
            'EXPRESSION': '"DN" = 1',
            'INPUT': outputs['PevstNaPolygonyRastrNaVektor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtrahovatPodleVrazu'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Minimální ohranièující geometrie
        alg_params = {
            'FIELD': 'fid',
            'INPUT': outputs['ExtrahovatPodleVrazu']['OUTPUT'],
            'TYPE': 3,  # Konvexní obal
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MinimlnOhraniujcGeometrie'] = processing.run('qgis:minimumboundinggeometry', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Extrahovat podle výrazu 2
        alg_params = {
            'EXPRESSION': 'area > 15000',
            'INPUT': outputs['MinimlnOhraniujcGeometrie']['OUTPUT'],
            'OUTPUT': parameters['Vysledekrastru']
        }
        outputs['ExtrahovatPodleVrazu2'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Vysledekrastru'] = outputs['ExtrahovatPodleVrazu2']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Rozdíl VT
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['ExtrahovatPodleVrazu2']['OUTPUT'],
            'OVERLAY': outputs['ObalovZnaVt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RozdlVt'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
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

        feedback.setCurrentStep(14)
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

        feedback.setCurrentStep(15)
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

        feedback.setCurrentStep(16)
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
        return 'model_komplet'

    def displayName(self):
        return 'model_komplet'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model_komplet()
