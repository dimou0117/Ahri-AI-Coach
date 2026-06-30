import os
import glob
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_folder, output_folder):
    """
    Convert all PascalVOC XML files in a folder to YOLO TXT format.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    xml_files = glob.glob(os.path.join(xml_folder, "*.xml"))
    print(f"Found {len(xml_files)} XML files to convert.")
    
    class_map = {"ahri": 0}  # Add more classes（if need）
    
    for xml_path in xml_files:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Image size
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        
        # Filename
        base_name = os.path.splitext(os.path.basename(xml_path))[0]
        txt_path = os.path.join(output_folder, base_name + ".txt")
        
        with open(txt_path, "w") as f:
            for obj in root.findall("object"):
                name = obj.find("name").text
                if name not in class_map:
                    print(f"Warning: Class '{name}' not in class_map, skipping.")
                    continue
                class_id = class_map[name]
                
                bndbox = obj.find("bndbox")
                xmin = float(bndbox.find("xmin").text)
                ymin = float(bndbox.find("ymin").text)
                xmax = float(bndbox.find("xmax").text)
                ymax = float(bndbox.find("ymax").text)
                
                # Convert to YOLO
                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                box_width = (xmax - xmin) / width
                box_height = (ymax - ymin) / height
                
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")
        
        print(f"Converted: {base_name}")
    
    print("Done!")

if __name__ == "__main__":
    
    XML_FOLDER = "label"
    
    OUTPUT_FOLDER = "label_yolo"
    
    convert_voc_to_yolo(XML_FOLDER, OUTPUT_FOLDER)
