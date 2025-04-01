import {get} from 'lodash'

// Convert units
const convert = (avfFiles, imdfFiles, getTranslations) => {
    const avf = avfFiles.units

    if (!avf) {
        return
    }

    const imdfFeatures = new Map(get(imdfFiles, 'unit.features', []).map((f) => [f.id, f]))

    const features = avf.features
        .map((feature) => {
            const id = get(feature, 'properties.UNIT_ID')
            const levelId = get(feature, 'properties.LEVEL_ID')

            const imdfFeature = imdfFeatures.get(id)
            if (imdfFeature) {
                return {...imdfFeature, geometry: get(feature, 'geometry', null)}
            }

            if (!levelId) {
                return null
            }

            return {
                id,
                type: 'Feature',
                feature_type: 'unit',
                geometry: get(feature, 'geometry'),
                properties: {
                    // Mandatory
                    level_id: levelId,
                    category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'unspecified',
                    // Optional
                    restriction: get(feature, 'properties.RESTRICTION') || null,
                    accessibility: get(feature, 'properties.ACCESSIBILITY') || null,
                    name: getTranslations(get(feature, 'properties.NAME') || null),
                    alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
                    display_point: get(feature, 'properties.DISPLAY_POINT') || null,
                },
            }
        })
        .filter(Boolean)

    imdfFiles.unit = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
