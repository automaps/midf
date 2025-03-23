import { get } from 'lodash'
import { v4 as uuidv4 } from 'uuid'

const convert = (avfFiles, imdfFiles, getTranslations) => {
  const avf = avfFiles.buildings

  if (!avf) {
    return
  }

  const imdfFeatures = new Map(get(imdfFiles, 'building.features', []).map((f) => [f.id, f]))

  const buildingFeatures = avf.features.map((feature) => {
    const id = get(feature, 'properties.BLDG_ID')

    const imdfFeature = imdfFeatures.get(id)
    if (imdfFeature) {
      return imdfFeature
    }

    return {
      id,
      type: 'Feature',
      feature_type: 'building',
      geometry: null,
      properties: {
        // Mandatory
        category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'unspecified',
        // Optional
        name: getTranslations(get(feature, 'properties.NAME') || null),
        alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
        restriction: get(feature, 'properties.RESTRICTION') || null,
        display_point: get(feature, 'properties.DISPLAY_POINT') || null,
        address_id: get(feature, 'properties.ADDRESS_ID') || null,
      },
    }
  })

  const footprintFeatures = avf.features
    .map((feature) => {
      const buildingId = get(feature, 'properties.BLDG_ID')

      // Skip footprint creation for the buildings those are already exist in the IMDF
      const imdfFeature = imdfFeatures.get(buildingId)
      if (imdfFeature) {
        return null
      }

      return {
        id: uuidv4(),
        type: 'Feature',
        feature_type: 'footprint',
        geometry: get(feature, 'geometry'),
        properties: {
          // Mandatory
          category: 'ground',
          building_ids: [buildingId],
          // Optional
          name: getTranslations(get(feature, 'properties.NAME', null)),
        },
      }
    })
    .filter(Boolean)

  imdfFiles.building = {
    type: 'FeatureCollection',
    features: buildingFeatures,
  }

  imdfFiles.footprint = {
    type: 'FeatureCollection',
    features: [...imdfFiles.footprint.features, ...footprintFeatures],
  }
}

export default convert
