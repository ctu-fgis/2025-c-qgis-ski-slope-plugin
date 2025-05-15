"""
Model exported as python.
Name : model
Group : 
With QGIS : 33412
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterPointCloudLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing

class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterPointCloudLayer('laz', 'LAZ', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Sjezd', 'sjezd', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
        results = {}
        outputs = {}

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

        feedback.setCurrentStep(1)
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

        feedback.setCurrentStep(2)
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

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Rastrový kalkulátor
        alg_params = {
            'CELL_SIZE': None,
            'CRS': 'ProjectCrs',
            'EXPRESSION': '"A@1">15  AND "A@1"<25',
            'EXTENT': None,
            'LAYERS': outputs['Sklon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RastrovKalkultor'] = processing.run('native:modelerrastercalc', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Převést na polygony (rastr na vektor)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RastrovKalkultor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PevstNaPolygonyRastrNaVektor'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extrahovat podle výrazu
        alg_params = {
            'EXPRESSION': '"DN" = 1',
            'INPUT': outputs['PevstNaPolygonyRastrNaVektor']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtrahovatPodleVrazu'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Minimální ohraničující geometrie
        alg_params = {
            'FIELD': 'fid',
            'INPUT': outputs['ExtrahovatPodleVrazu']['OUTPUT'],
            'TYPE': 3,  # Konvexní obal
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MinimlnOhraniujcGeometrie'] = processing.run('qgis:minimumboundinggeometry', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Extrahovat podle výrazu
        alg_params = {
            'EXPRESSION': 'area > 15000',
            'INPUT': outputs['MinimlnOhraniujcGeometrie']['OUTPUT'],
            'OUTPUT': parameters['Sjezd']
        }
        outputs['ExtrahovatPodleVrazu'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Sjezd'] = outputs['ExtrahovatPodleVrazu']['OUTPUT']
        return results

    def name(self):
        return 'model'

    def displayName(self):
        return 'model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()
