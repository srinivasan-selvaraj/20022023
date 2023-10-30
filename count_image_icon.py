
import fitz

class ExtractImages:

    def __init__(self, left, right) -> None:
        self.files = [left, right]

    def extract_image_icons(self):
        images_icons = []
        for file in self.files:
            doc = fitz.open(file)
            temp = {}
            for page_index in range(len(doc)):
                icons = doc[page_index].get_xobjects()
                temp["icons"] = [(i[0], i[3]) for i in icons]
                image_list = doc[page_index].get_images(full=True)
                print(image_list,file)
                temp["count_images"] = len(image_list)
                images_icons.append(temp)
        return images_icons

    def get_insertions(self,data):
        return len([x for x in data if (list(x[1])[0] >= 0 and list(x[1])[1] >= 0) ])
    
    def icons_compare2(self, icons):
        page_icons = icons['icons']
        count_img = icons['count_images']
        data1 = page_icons[0]
        data2 = page_icons[1]
        result1 = self.get_insertions(data1)
        result2 = self.get_insertions(data2)
        icon_ =  (result1,result2)
        print(count_img,"images")
        print(icon_,"icons")
        result = [x + y for x, y in zip(icon_,count_img)]
        return result
                        

    def compare(self):
        dat = self.extract_image_icons()
        right_value = dat[1]
        left_value = dat[0]
        pages = set(list(right_value.keys()) + list(left_value.keys()))
        output = {}
        for i in pages:
            output[f'{i}'] = (left_value[i] if left_value.get(
                i) else 0, right_value[i] if right_value.get(i) else 0)
        result = self.icons_compare2(output)
        return result


"""
TC_AR_009.pdf - inserted one
TC_AR_010.pdf - deleted one
TC_AR_011.pdf - deleted icon and replaced the images
TC_AR_012.pdf - deleted icon and replaced the icons
"""
files = ["TC_AR_009.pdf", "TC_AR_010.pdf", "TC_AR_011.pdf", "TC_AR_012.pdf"]

ext_img = ExtractImages(left="TC_AR_011.pdf", right="TC_AR_012.pdf")

final_output = ext_img.compare()

print(final_output)
