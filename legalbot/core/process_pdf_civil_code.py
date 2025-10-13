"""
PDF Civil Code Processor for MyzamAI
Processes PDF documents of Civil Code of Kyrgyz Republic
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import PyPDF2
    import fitz  # PyMuPDF
except ImportError:
    print("Installing required PDF libraries...")
    import subprocess
    subprocess.run(["pip", "install", "PyPDF2", "PyMuPDF"], check=True)
    import PyPDF2
    import fitz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CivilCodePDFProcessor:
    """
    Processes PDF documents of Civil Code and extracts articles
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF (fitz)
        """
        logger.info(f"Extracting text from {pdf_path}...")
        
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
                text += "\n"  # Add page break
                
            doc.close()
            logger.info(f"✓ Extracted text from {doc.page_count} pages")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting from {pdf_path}: {e}")
            return ""
    
    def parse_articles(self, text: str) -> List[Dict[str, str]]:
        """
        Parse articles from extracted text
        """
        logger.info("Parsing articles from text...")
        
        articles = []
        
        # Pattern to match article numbers and content
        # Look for patterns like "Статья 1.", "Статья 2.", etc.
        article_pattern = r'Статья\s+(\d+)[\.\s]*(.*?)(?=Статья\s+\d+|\Z)'
        
        matches = re.finditer(article_pattern, text, re.DOTALL | re.MULTILINE)
        
        for match in matches:
            article_num = match.group(1)
            content = match.group(2).strip()
            
            # Clean up content
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            content = content.replace('\n', ' ').strip()
            
            if content and len(content) > 10:  # Filter out empty or very short articles
                articles.append({
                    'number': int(article_num),
                    'title': f"Статья {article_num}",
                    'content': content,
                    'source': f"Гражданский кодекс КР, статья {article_num}"
                })
        
        logger.info(f"✓ Parsed {len(articles)} articles")
        return articles
    
    def process_pdf_file(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Process a single PDF file
        """
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return []
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return []
        
        # Parse articles
        articles = self.parse_articles(text)
        
        return articles
    
    def process_all_pdfs(self, pdf_files: List[str]) -> List[Dict[str, str]]:
        """
        Process all PDF files and combine articles
        """
        all_articles = []
        
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file}...")
            articles = self.process_pdf_file(pdf_file)
            all_articles.extend(articles)
        
        # Sort by article number
        all_articles.sort(key=lambda x: x['number'])
        
        logger.info(f"✓ Total articles processed: {len(all_articles)}")
        return all_articles
    
    def save_articles_to_file(self, articles: List[Dict[str, str]], output_file: str):
        """
        Save articles to text file
        """
        logger.info(f"Saving articles to {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for article in articles:
                f.write(f"Статья {article['number']}\n")
                f.write(f"{article['content']}\n\n")
                f.write("=" * 80 + "\n\n")
        
        logger.info(f"✓ Saved {len(articles)} articles to {output_file}")
    
    def create_article_chunks(self, articles: List[Dict[str, str]], chunk_size: int = 1000) -> List[str]:
        """
        Create text chunks for FAISS indexing
        """
        logger.info(f"Creating chunks of size {chunk_size}...")
        
        chunks = []
        
        for article in articles:
            content = article['content']
            
            # If article is short, use as is
            if len(content) <= chunk_size:
                chunks.append(f"Статья {article['number']}: {content}")
            else:
                # Split long articles into chunks
                words = content.split()
                for i in range(0, len(words), chunk_size // 10):  # Approximate word count
                    chunk_words = words[i:i + chunk_size // 10]
                    chunk_text = ' '.join(chunk_words)
                    if len(chunk_text) > 50:  # Only add substantial chunks
                        chunks.append(f"Статья {article['number']} (часть): {chunk_text}")
        
        logger.info(f"✓ Created {len(chunks)} chunks")
        return chunks


def main():
    """
    Main function to process PDF files
    """
    # Initialize processor
    processor = CivilCodePDFProcessor("data")
    
    # PDF files to process
    pdf_files = [
        "data/civil_code_part1.pdf",  # Articles 1-414
        "data/civil_code_part2.pdf"   # Articles 415-1208
    ]
    
    # Check if PDF files exist
    missing_files = [f for f in pdf_files if not os.path.exists(f)]
    if missing_files:
        logger.error(f"Missing PDF files: {missing_files}")
        logger.info("Please place the PDF files in the data/ directory:")
        logger.info("1. civil_code_part1.pdf (Articles 1-414)")
        logger.info("2. civil_code_part2.pdf (Articles 415-1208)")
        return
    
    # Process all PDFs
    articles = processor.process_all_pdfs(pdf_files)
    
    if not articles:
        logger.error("No articles found in PDF files")
        return
    
    # Save to text file
    processor.save_articles_to_file(articles, "data/civil_code_full.txt")
    
    # Create chunks for FAISS
    chunks = processor.create_article_chunks(articles)
    
    # Save chunks
    with open("data/civil_code_chunks.txt", 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + "\n\n")
    
    logger.info("✅ PDF processing completed!")
    logger.info(f"📊 Statistics:")
    logger.info(f"   - Total articles: {len(articles)}")
    logger.info(f"   - Total chunks: {len(chunks)}")
    logger.info(f"   - Output files:")
    logger.info(f"     - data/civil_code_full.txt")
    logger.info(f"     - data/civil_code_chunks.txt")


if __name__ == "__main__":
    main()
