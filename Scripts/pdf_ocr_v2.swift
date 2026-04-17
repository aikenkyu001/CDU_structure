import Foundation
import Vision
import Quartz

let pdfDir = "References/PDF"
let fileManager = FileManager.default

guard let files = try? fileManager.contentsOfDirectory(atPath: pdfDir) else {
    print("Could not read directory")
    exit(1)
}

for file in files where file.hasSuffix(".pdf") {
    let pdfPath = "\(pdfDir)/\(file)"
    let txtPath = "\(pdfDir)/\(file.replacingOccurrences(of: ".pdf", with: ".txt"))"
    
    // Skip if TXT already exists and is not empty
    if fileManager.fileExists(atPath: txtPath), let attr = try? fileManager.attributesOfItem(atPath: txtPath), (attr[.size] as? Int64 ?? 0) > 100 {
        continue
    }

    print("Processing: \(file)")
    
    guard let pdfDocument = PDFDocument(url: URL(fileURLWithPath: pdfPath)) else {
        print("Failed to load PDF: \(file)")
        continue
    }
    
    var fullText = ""
    for i in 0..<pdfDocument.pageCount {
        guard let page = pdfDocument.page(at: i) else { continue }
        if let pageText = page.string {
            fullText += pageText + "\n"
        }
    }
    
    if !fullText.isEmpty {
        try? fullText.write(toFile: txtPath, atomically: true, encoding: .utf8)
        print("Saved: \(txtPath)")
    }
}
