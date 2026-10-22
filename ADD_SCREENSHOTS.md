# Adding Screenshots to Your Paper

## 📸 Screenshots Needed

You need 2 screenshots for the paper:

### Screenshot 1: Dataset Management Interface
**What to capture:**
- Go to http://localhost:5175
- Click "Dataset Management"
- Show the upload area and uploaded datasets list
- Make sure at least one dataset is visible

**File name:** `dataset_management.png`

### Screenshot 2: Analysis Results Interface  
**What to capture:**
- Go to "Flaky Test Analysis"
- Run an analysis with Random Forest
- Capture the results showing:
  - Summary statistics (22 flaky, 115 stable)
  - Feature importance chart
  - At least 2-3 test predictions with recommendations

**File name:** `analysis_results.png`

---

## 🖼️ How to Take Screenshots

### On macOS:
1. Press **Cmd + Shift + 4**
2. Press **Spacebar** to capture full window
3. Click the browser window
4. Screenshot saves to Desktop

### On Windows:
1. Press **Windows + Shift + S**
2. Select the area you want
3. Screenshot goes to clipboard
4. Paste into Paint and save

---

## 📝 How to Add to LaTeX Paper

### Step 1: Save Screenshots
Put both PNG files in the project directory:
```
Innovative/
├── dataset_management.png
├── analysis_results.png
└── term_paper.tex
```

### Step 2: Update LaTeX Code

Find these placeholder sections in `term_paper.tex`:

```latex
\begin{figure}[h]
\centering
\fbox{\parbox{0.45\textwidth}{\centering\textit{[Screenshot: Dataset Management Interface\\showing upload area and dataset list]}}}
\caption{Dataset Management Interface}
\label{fig:dataset}
\end{figure}
```

Replace with:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{dataset_management.png}
\caption{Dataset Management Interface}
\label{fig:dataset}
\end{figure}
```

And:

```latex
\begin{figure}[h]
\centering
\fbox{\parbox{0.45\textwidth}{\centering\textit{[Screenshot: Analysis Results Interface\\showing model comparison and predictions]}}}
\caption{Flaky Test Analysis Results}
\label{fig:analysis}
\end{figure}
```

Replace with:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{analysis_results.png}
\caption{Flaky Test Analysis Results}
\label{fig:analysis}
\end{figure}
```

---

## 🎯 Quick Instructions

1. **Make sure app is running** at http://localhost:5175
2. **Take Screenshot 1:** Dataset Management page with uploaded data
3. **Take Screenshot 2:** Analysis Results page with predictions
4. **Save as:** `dataset_management.png` and `analysis_results.png`
5. **Put in project folder** (same directory as term_paper.tex)
6. **Update LaTeX:** Replace placeholder text with `\includegraphics` commands
7. **Compile:** Either use Overleaf or run `./COMPILE_PAPER.sh`

---

## 📤 Using Overleaf

If using Overleaf:
1. Upload `term_paper.tex` to Overleaf
2. Click "Upload" button in Overleaf
3. Upload both PNG screenshot files
4. Recompile
5. Screenshots will appear in the PDF

---

## ✅ Checklist

- [ ] App is running
- [ ] Screenshot 1 taken (Dataset Management)
- [ ] Screenshot 2 taken (Analysis Results)
- [ ] Both saved as PNG files
- [ ] Files in correct location
- [ ] LaTeX updated with `\includegraphics`
- [ ] Paper compiled successfully
- [ ] Screenshots visible in PDF

---

**Note:** The placeholders are already in the paper, so it will compile without errors. You can submit with placeholders, or add real screenshots for a better presentation.
