import convertVenue from './convertVenue'
import convertBuildings from './convertBuildings'
import convertLevels from './convertLevels'
import convertSections from './convertSections'
import convertFixtures from './convertFixtures'
import convertOpenings from './convertOpenings'
import convertUnits from './convertUnits'
import convertAnchors from './convertAnchors'
import convertPoints from './convertPoints'
import convertOccupants from './convertOccupants'
import parseCategories from '../parseCategories'
import createTranslationsGetter from '../../utils/translations/createTranslationsGetter'

const EMPTY_GEOJSON = () => ({ type: 'FeatureCollection', features: [] })

function convert(avfFiles, originalIMDFFiles) {
  const imdfFiles = {
    address: EMPTY_GEOJSON(),
    amenity: EMPTY_GEOJSON(),
    anchor: EMPTY_GEOJSON(),
    building: EMPTY_GEOJSON(),
    detail: EMPTY_GEOJSON(),
    fixture: EMPTY_GEOJSON(),
    footprint: EMPTY_GEOJSON(),
    geofence: EMPTY_GEOJSON(),
    kiosk: EMPTY_GEOJSON(),
    level: EMPTY_GEOJSON(),
    occupant: EMPTY_GEOJSON(),
    opening: EMPTY_GEOJSON(),
    relationship: EMPTY_GEOJSON(),
    section: EMPTY_GEOJSON(),
    unit: EMPTY_GEOJSON(),
    venue: EMPTY_GEOJSON(),
  }

  // Fill the future exported files with original IMDF files
  Object.keys(imdfFiles).forEach((key) => {
    if (originalIMDFFiles[key]) {
      imdfFiles[key] = originalIMDFFiles[key]
    }
  })

  // Prepare categories for use in Points and Occupants converters
  // Export only Points/Occupants which have corresponding imdf category
  const { flatten: flattenCategories } = parseCategories(avfFiles.categories)
  const imdfCategories = new Map(
    flattenCategories.filter(({ imdf }) => Boolean(imdf)).map((c) => [c.id, c]),
  )

  // Make tranlations getter
  const getTranslations = createTranslationsGetter(avfFiles.dictionary)

  // Convert AVF to IMDF
  convertVenue(avfFiles, imdfFiles, getTranslations)
  convertBuildings(avfFiles, imdfFiles, getTranslations)
  convertLevels(avfFiles, imdfFiles, getTranslations)
  convertSections(avfFiles, imdfFiles, getTranslations)
  convertFixtures(avfFiles, imdfFiles, getTranslations)
  convertOpenings(avfFiles, imdfFiles, getTranslations)
  convertUnits(avfFiles, imdfFiles, getTranslations)
  convertPoints(avfFiles, imdfFiles, imdfCategories, getTranslations)
  convertOccupants(avfFiles, imdfFiles, imdfCategories, getTranslations)
  convertAnchors(avfFiles, imdfFiles, imdfCategories)

  // Create imdf manifest
  imdfFiles.manifest = {
    version: '1.0.0',
    created: new Date(),
    generated_by: 'Point-Maps CMS',
    language: 'en-US',
  }

  return imdfFiles
}

export default convert
