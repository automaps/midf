import {get} from 'lodash'

const convert = (avfFiles, imdfFiles, getTranslations) => {
    const avf = avfFiles.sections

    if (!avf) {
        return
    }

    const imdfFeatures = new Map(get(imdfFiles, 'section.features', []).map((f) => [f.id, f]))

    const features = avf.features
        .map((feature) => {
            const id = get(feature, 'properties.SECTION_ID')
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
                feature_type: 'section',
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
                    address_id: get(feature, 'properties.ADDRESS_ID') || null,
                    correlation_id: get(feature, 'properties.CORRELATION_ID') || null,
                    parents: get(feature, 'properties.PARENTS') || null,
                },
            }
        })
        .filter(Boolean)

    imdfFiles.section = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
