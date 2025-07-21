import {get} from 'lodash'
import {v4 as uuidv4} from 'uuid'

const getLink = (website) =>
    website && (website.startsWith('http') ? website : `https://${website}`)

const convert = (avfFiles, imdfFiles, categories, getTranslations) => {
    const avf = avfFiles.occupants

    if (!avf) {
        return
    }

    const features = avf.features
        .map((feature) => {
            const category = categories.get(get(feature, 'properties.CATEGORY_ID'))

            if (!category) {
                return null
            }

            // Export based on a poiType at the POI's category
            if (category.poiType !== 'occupants') {
                return null
            }

            let anchorId = get(feature, 'properties.ANCHOR_ID')

            if (!anchorId) {
                anchorId = uuidv4()
                feature.properties.ANCHOR_ID = anchorId
            }

            const unitId = get(feature, 'properties.UNIT_ID')

            // We can't export occupant without UNIT_ID and ANCHOR_ID fields because
            // they are required for generating corresponding Anchor
            if (!unitId) {
                return null
            }

            // The NAME of the occupant is a mandatory field
            const name = getTranslations(get(feature, 'properties.NAME'))

            if (!name) {
                return null
            }

            return {
                id: get(feature, 'properties.OCCU_ID'),
                type: 'Feature',
                feature_type: 'occupant',
                geometry: null,
                properties: {
                    // Mandatory
                    name,
                    anchor_id: anchorId,
                    category: category.imdf,
                    // Optional
                    hours: get(feature, 'properties.HOURS') || null,
                    phone: get(feature, 'properties.PHONE') || null,
                    website: getLink(get(feature, 'properties.WEBSITE')) || null,
                    validity: get(feature, 'properties.VALIDITY') || null,
                    correlation_id: get(feature, 'properties.CORRELATION_ID') || null,
                },
            }
        })
        .filter(Boolean)

    imdfFiles.occupant = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
