import {get} from 'lodash'

const convert = (avfFiles, imdfFiles, getTranslations) => {
    const avf = avfFiles.openings

    if (!avf) {
        return
    }

    const imdfFeatures = new Map(get(imdfFiles, 'opening.features', []).map((f) => [f.id, f]))

    const features = avf.features
        .map((feature) => {
            const id = get(feature, 'properties.OPENING_ID')
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
                feature_type: 'opening',
                geometry: get(feature, 'geometry'),
                properties: {
                    // Mandatory
                    level_id: levelId,
                    category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'pedestrian',
                    // Optional
                    accessibility: get(feature, 'properties.ACCESSIBILITY') || null,
                    access_control: get(feature, 'properties.ACCESS_CONTROL') || null,
                    door: get(feature, 'properties.DOOR') || null,
                    name: getTranslations(get(feature, 'properties.NAME') || null),
                    alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
                    display_point: get(feature, 'properties.DISPLAY_POINT') || null,
                },
            }
        })
        .filter(Boolean)

    imdfFiles.opening = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
