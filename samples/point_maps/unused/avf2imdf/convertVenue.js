import { get } from 'lodash'

const convert = (avfFiles, imdfFiles, getTranslations) => {
  const avf = avfFiles.venue

  if (!avf) {
    return
  }

  const imdfFeatures = new Map(get(imdfFiles, 'venue.features', []).map((f) => [f.id, f]))

  const features = avf.features.map((feature) => {
    const id = get(feature, 'properties.VENUE_ID')

    const imdfFeature = imdfFeatures.get(id)
    if (imdfFeature) {
      return { ...imdfFeature, geometry: get(feature, 'geometry', null) }
    }

    const name = getTranslations(get(feature, 'properties.NAME'))
    if (!name) {
      throw new Error('The NAME field of the Venue must be set')
    }

    const addressId = get(feature, 'properties.ADDRESS_ID')
    if (!addressId) {
      throw new Error('The ADDRESS_ID field of the Venue must be set')
    }

    const displayPoint = get(feature, 'properties.DISPLAY_POINT')
    if (!displayPoint) {
      throw new Error('The DISPLAY_POINT field of the Venue must be set')
    }

    return {
      id,
      type: 'Feature',
      feature_type: 'venue',
      geometry: get(feature, 'geometry'),
      properties: {
        // Mandatory
        name,
        address_id: get(feature, 'properties.ADDRESS_ID'),
        display_point: get(feature, 'properties.DISPLAY_POINT'),
        category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'unspecified',
        // Optional
        restriction: get(feature, 'properties.RESTRICTION') || null,
        alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
        hours: get(feature, 'properties.HOURS') || null,
        website: get(feature, 'properties.WEBSITE') || null,
        phone: get(feature, 'properties.PHONE') || null,
      },
    }
  })

  imdfFiles.venue = {
    type: 'FeatureCollection',
    features,
  }
}

export default convert
