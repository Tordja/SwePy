from Autodesk.Revit.DB import *
from collections import Counter
from itertools import izip, groupby
import json
import io
import os

doc = __revit__.ActiveUIDocument.Document

links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
arcname = "Konsertarenaen"
filepath = doc.PathName

def linkgetter(linkname):

	for l in links:
		if linkname in l.Name:
			return l.GetLinkDocument()
			
			

def fixtures():
	plumbfix = FilteredElementCollector(linkgetter(arcname)).OfCategory(BuiltInCategory.OST_PlumbingFixtures).WhereElementIsNotElementType().ToElements()
	plumbfixfam = [plumb.Symbol.Family.Name for plumb in plumbfix]
	plumblevel = [linkgetter(arcname).GetElement(plumb.LevelId).Name for plumb in plumbfix]
	
	return [plumblevel, plumbfixfam]



def sortingfunction(elements):

	newlist = {}
	temp = {}

	transposed = map(list, zip(*elements))
	
	f = lambda x: x[0]
	
	for key, group in groupby(sorted(transposed), key=f):
		newlist[key] = list(group)
	
	for key, value in newlist.iteritems():
		vals = [v[1] for v in value]
		temp[key] = Counter(vals)
	
	return temp
	

	
if __name__ == '__main__':

	data = sortingfunction(fixtures())
	path = filepath[:-4]+' Arcdata'
	
	if not os.path.isdir(path):
		os.makedirs(path)
	
	with io.open(r'{0}\Arcdata.txt'.format(path), 'w', encoding='utf-8') as outfile:
		outfile.write(json.dumps(data, ensure_ascii = False))
