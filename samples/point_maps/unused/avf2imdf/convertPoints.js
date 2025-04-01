import {get} from 'lodash'

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
            if (category.poiType !== 'amenities') {
                return null
            }

            const unitId = get(feature, 'properties.UNIT_ID')

            if (!unitId) {
                return null
            }

            return {
                id: get(feature, 'properties.OCCU_ID'),
                type: 'Feature',
                feature_type: 'amenity',
                geometry: get(feature, 'geometry'),
                properties: {
                    // Mandatory
                    category: category.imdf,
                    unit_ids: get(feature, 'properties.UNIT_IDS') || [unitId],
                    // Optional
                    accessibility: get(feature, 'properties.ACCESSIBILITY') || null,
                    name: getTranslations(get(feature, 'properties.NAME') || null),
                    alt_name: getTranslations(get(feature, 'properties.ALT_NAME') || null),
                    hours: get(feature, 'properties.HOURS') || null,
                    phone: get(feature, 'properties.PHONE') || null,
                    website: getLink(get(feature, 'properties.WEBSITE')) || null,
                    address_id: get(feature, 'properties.ADDRESS_ID') || null,
                    correlation_id: get(feature, 'properties.CORRELATION_ID') || null,
                },
            }
        })
        .filter(Boolean)

    imdfFiles.amenity = {
        type: 'FeatureCollection',
        features,
    }
}

export default convert
