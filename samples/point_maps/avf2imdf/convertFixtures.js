import { get } from 'lodash'

const convert = (avfFiles, imdfFiles, getTranslations) => {
  const avf = avfFiles.fixtures

  if (!avf) {
    return
  }

  const imdfFeatures = new Map(get(imdfFiles, 'fixture.features', []).map((f) => [f.id, f]))

  const features = avf.features
    .map((feature) => {
      const id = get(feature, 'properties.FIXTURE_ID')
      const levelId = get(feature, 'properties.LEVEL_ID')

      const imdfFeature = imdfFeatures.get(id)
      if (imdfFeature) {
        return { ...imdfFeature, geometry: get(feature, 'geometry', null) }
      }

      if (!levelId) {
        return null
      }

      return {
        id,
        type: 'Feature',
        feature_type: 'fixture',
        geometry: get(feature, 'geometry'),
        properties: {
          // Mandatory
          level_id: levelId,
          category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'unspecified',
          // Optional
          name: getTranslations(get(feature, 'properties.NAME') || null),
          alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
          anchor_id: get(feature, 'properties.ANCHOR_ID') || null,
          display_point: get(feature, 'properties.DISPLAY_POINT') || null,
        },
      }
    })
    .filter(Boolean)

  imdfFiles.fixture = {
    type: 'FeatureCollection',
    features,
  }
}

export default convert
