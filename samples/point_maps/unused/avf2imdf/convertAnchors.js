import {get} from 'lodash'

const convert = (avfFiles, imdfFiles, categories) => {
    const occupants = avfFiles.occupants

    if (!occupants) {
        return
    }

    const units = new Map(avfFiles.units.features.map((unit) => [unit.properties.UNIT_ID, unit]))

    const imdfUnitAddresses = get(imdfFiles, 'anchor.features', []).reduce(
        (acc, {properties: {unit_id, address_id}}) => {
            const addresses = acc.get(unit_id) || []
            addresses.push(address_id)
            acc.set(unit_id, addresses)
            return acc
        },
        new Map(),
    )

    const features = occupants.features
        .map((feature) => {
            const category = categories.get(get(feature, 'properties.CATEGORY_ID'))

            // skip if there is no a corresponding imdf category
            if (!category) {
                return null
            }

            // skip if it's an amenity type
            if (category.poiType === 'amenities') {
                return null
            }

            const anchorId = get(feature, 'properties.ANCHOR_ID')
            const unitId = get(feature, 'properties.UNIT_ID')

            if (!anchorId || !unitId) {
                return null
            }

            const unit = units.get(unitId)
            let addressId = (unit && unit.properties.ADDRESS_ID) || null

            if (!addressId) {
                const unitAddresses = imdfUnitAddresses.get(unitId)
                addressId = unitAddresses ? unitAddresses.pop() : null
            }

            return {
                id: anchorId,
                type: 'Feature',
                feature_type: 'anchor',
                geometry: get(feature, 'geometry'),
                properties: {
                    // Mandatory
                    unit_id: unitId,
                    // Optional
                    address_id: addressId,
                },
            }
        })
        .filter(Boolean)

    // Keep imdf original Anchors those used in kiosk and fixture
    const kioskFixtureIDs = new Set([
        ...get(imdfFiles, 'kiosk.features', []).map((f) => f.properties.anchor_id),
        ...get(imdfFiles, 'fixture.features', []).map((f) => f.properties.anchor_id),
    ])
    const kioskFixtureAnchors = get(imdfFiles, 'anchor.features', []).filter((f) =>
        kioskFixtureIDs.has(f.id),
    )

    // Keep original addresses
    const addressIDs = new Set(get(imdfFiles, 'address.features', []).map((f) => f.id))
    const addressAnchors = get(imdfFiles, 'anchor.features', []).filter((f) =>
        addressIDs.has(f.properties.address_id),
    )

    // avoid duplicating of anchors which is possible if one anchor is used by
    // multiple occupants
    const uniqFeatures = new Map(
        [...features, ...kioskFixtureAnchors, ...addressAnchors].map((f) => [f.id, f]),
    ).values()

    imdfFiles.anchor = {
        type: 'FeatureCollection',
        features: Array.from(uniqFeatures),
    }
}

export default convert
