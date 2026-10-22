#!/bin/bash
# Script to create LaTeX submission package

echo "Creating LaTeX Submission Package..."

# Create a temporary directory
mkdir -p latex_submission

# Copy LaTeX source
cp term_paper.tex latex_submission/

# Copy README
cp LATEX_README.txt latex_submission/

# Copy screenshots if they exist (you need to add these from Overleaf)
if [ -f dataset_management.png ]; then
    cp dataset_management.png latex_submission/
    echo "✓ Added dataset_management.png"
else
    echo "⚠ Warning: dataset_management.png not found"
    echo "  Please download from Overleaf and add to ZIP"
fi

if [ -f analysis_results.png ]; then
    cp analysis_results.png latex_submission/
    echo "✓ Added analysis_results.png"
else
    echo "⚠ Warning: analysis_results.png not found"
    echo "  Please download from Overleaf and add to ZIP"
fi

# Copy PDF if it exists
if [ -f term_paper.pdf ]; then
    cp term_paper.pdf latex_submission/
    echo "✓ Added term_paper.pdf"
else
    echo "⚠ Warning: term_paper.pdf not found"
    echo "  Please compile on Overleaf first"
fi

# Create ZIP file
cd latex_submission
zip -r ../FlakeGuard_AI_LaTeX_Submission.zip *
cd ..

# Cleanup
rm -rf latex_submission

echo ""
echo "✅ Created: FlakeGuard_AI_LaTeX_Submission.zip"
echo ""
echo "Contents:"
unzip -l FlakeGuard_AI_LaTeX_Submission.zip
echo ""
echo "Next steps:"
echo "1. Download screenshots and PDF from Overleaf"
echo "2. Add them to the project directory"
echo "3. Run this script again to create complete ZIP"
