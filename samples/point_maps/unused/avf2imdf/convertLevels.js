import {get} from 'lodash'

const convert = (avfFiles, imdfFiles, getTranslations) => {
    const avf = avfFiles.levels

    if (!avf) {
        return
    }

    const imdfFeatures = new Map(get(imdfFiles, 'level.features', []).map((f) => [f.id, f]))

    const features = avf.features.map((feature) => {
        const id = get(feature, 'properties.LEVEL_ID')

        const name = getTranslations(get(feature, 'properties.NAME'))
        if (!name) {
            throw new Error('The NAME field of the Level must be set')
        }

        const short_name = getTranslations(get(feature, 'properties.SHORT_NAME'))
        if (!short_name) {
            throw new Error('The SHORT_NAME field of the Level must be set')
        }

        const imdfFeature = imdfFeatures.get(id)
        if (imdfFeature) {
            imdfFeature.properties.name = name
            imdfFeature.properties.short_name = short_name
            return {...imdfFeature, geometry: get(feature, 'geometry', null)}
        }

        return {
            id,
            type: 'Feature',
            feature_type: 'level',
            geometry: get(feature, 'geometry'),
            properties: {
                // Mandatory
                outdoor: get(feature, 'properties.OUTDOOR', false),
                ordinal: get(feature, 'properties.ORDINAL', 0),
                name,
                short_name,
                category: feature?.properties?.CATEGORY?.toLowerCase() ?? 'unspecified',
                // Optional
                restriction: get(feature, 'properties.RESTRICTION') || null,
                display_point: get(feature, 'properties.DISPLAY_POINT') || null,
                address_id: get(feature, 'properties.ADDRESS_ID') || null,
                building_ids: get(feature, 'properties.BLDG_IDS') || null,
            },
        }
    })

    imdfFiles.level = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
