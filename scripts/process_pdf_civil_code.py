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
        Extract text from PDF using PyMuPDF (fitz) with better error handling
        """
        logger.info(f"Extracting text from {pdf_path}...")
        
        try:
            # Try to open with different methods
            doc = None
            text = ""
            
            # Method 1: Try PyMuPDF (fitz)
            try:
                doc = fitz.open(pdf_path)
                logger.info(f"✓ Opened PDF with PyMuPDF: {doc.page_count} pages")
                
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    page_text = page.get_text()
                    if page_text.strip():  # Only add non-empty pages
                        text += page_text
                        text += "\n"  # Add page break
                
                doc.close()
                logger.info(f"✓ Extracted text from {doc.page_count} pages")
                return text
                
            except Exception as e1:
                logger.warning(f"PyMuPDF failed: {e1}")
                
                # Method 2: Try PyPDF2 as fallback
                try:
                    import PyPDF2
                    with open(pdf_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        logger.info(f"✓ Opened PDF with PyPDF2: {len(pdf_reader.pages)} pages")
                        
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()
                            if page_text.strip():  # Only add non-empty pages
                                text += page_text
                                text += "\n"
                        
                        logger.info(f"✓ Extracted text from {len(pdf_reader.pages)} pages")
                        return text
                        
                except Exception as e2:
                    logger.error(f"PyPDF2 also failed: {e2}")
                    return ""
            
        except Exception as e:
            logger.error(f"Error extracting from {pdf_path}: {e}")
            return ""
    
    def parse_articles(self, text: str) -> List[Dict[str, str]]:
        """
        Parse articles from extracted text with improved patterns
        """
        logger.info("Parsing articles from text...")
        
        articles = []
        
        # Split text into lines for better processing
        lines = text.split('\n')
        current_article = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts a new article
            article_match = re.match(r'^Статья\s+(\d+)', line, re.IGNORECASE)
            if article_match:
                # Save previous article if exists
                if current_article is not None and current_content:
                    content = ' '.join(current_content).strip()
                    # Clean up content - remove chapter headers and other artifacts
                    content = self._clean_article_content(content)
                    if content and len(content) > 20:
                        articles.append({
                            'number': current_article,
                            'title': f"Статья {current_article}",
                            'content': content,
                            'source': f"Гражданский кодекс КР, статья {current_article}"
                        })
                
                # Start new article
                current_article = int(article_match.group(1))
                current_content = [line]
            else:
                # Add to current article content
                if current_article is not None:
                    current_content.append(line)
        
        # Don't forget the last article
        if current_article is not None and current_content:
            content = ' '.join(current_content).strip()
            if content and len(content) > 20:
                articles.append({
                    'number': current_article,
                    'title': f"Статья {current_article}",
                    'content': content,
                    'source': f"Гражданский кодекс КР, статья {current_article}"
                })
        
        # Sort by article number
        articles.sort(key=lambda x: x['number'])
        
        logger.info(f"✓ Parsed {len(articles)} articles")
        return articles
    
    def _clean_article_content(self, content: str) -> str:
        """
        Clean article content by removing chapter headers and other artifacts
        """
        # Remove chapter headers and section titles
        patterns_to_remove = [
            r'Глава \d+.*?$',
            r'Параграф \d+.*?$',
            r'Раздел \d+.*?$',
            r'Имущественный наем.*?$',
            r'Общие положения.*?$',
            r'Договор.*?найма.*?$'
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Remove content that appears to be from next chapter
        # Look for patterns that indicate chapter boundaries
        chapter_boundaries = [
            'Глава', 'Параграф', 'Раздел', 'Имущественный наем', 'Общие положения'
        ]
        
        # Find the last occurrence of article content before chapter headers
        for boundary in chapter_boundaries:
            if boundary in content:
                # Find the position of the boundary
                pos = content.find(boundary)
                if pos > 0:
                    # Keep only content before the boundary
                    content = content[:pos].strip()
                    break
        
        # Remove next article if it's included in the same chunk
        # Look for "Статья" followed by a number that's not the current article
        article_pattern = r'Статья \d+'
        matches = list(re.finditer(article_pattern, content))
        
        if len(matches) > 1:
            # Keep only the first article (the requested one)
            first_match = matches[0]
            second_match = matches[1]
            content = content[:second_match.start()].strip()
        
        return content
    
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
