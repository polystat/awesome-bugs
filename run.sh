# Install dependencies
apt-get update -y
apt-get install -y clang-tidy cmake
python3.10 -m pip install --upgrade pip wheel
python3.10 -m pip install -r scripts/requirements.txt
python3.10 -m pip install -e ./scripts

# Extracting source files from correct YAML files
echo "Collecting sources"
[[ -z $1 ]] && glob="" || glob=$1
echo "Using GLOB filter for sources: $glob"
python3.10 -m source_files_extractor tests temp/sources "$glob"
echo "Sources are collected"

# Run Clang-Tidy and save reports to "results" folder
python3.10 -m build_sources temp/sources build
echo "Clang-Tidy analysis has started"
python3.10 -m clang_tidy -p ./build > results/clang-out.txt
echo "Clang-Tidy analysis has finished"

# Run Polystat (EO) and save reports to "results" folder
curl -L -o polystat.jar "https://github.com/polystat/polystat-cli/releases/download/v0.1.11/polystat.jar"
echo "Polystat (EO) analysis has started"
java -jar polystat.jar eo --in temp/sources/eo --to file=results/polystat-eo-out.txt --sarif
echo "Polystat (EO) analysis has finished"

# Run Polystat (Java via J2EO) and save reports to "results" folder
curl -L -o j2eo.jar "https://search.maven.org/remotecontent?filepath=org/polystat/j2eo/0.5.3/j2eo-0.5.3.jar"
java -jar j2eo.jar temp/sources/java -o temp/sources/j2eo
echo "Polystat (Java via J2EO) analysis has started"
java -jar polystat.jar eo --in temp/sources/j2eo --to file=results/polystat-j2eo-out.txt --sarif
echo "Polystat (Java via J2EO) analysis has finished"

# SVF analysis
echo "SVF build has started"
cd SVF
source ./build.sh
cd ../
echo "SVF build has finished"
echo "SVF analysis has started"
python3.10 -m SVF temp/sources/cpp temp/bc results SVF/Release-build/bin
echo "SVF analysis has finished"

# Cppcheck
sudo apt-get install -y cppcheck
echo "Cppcheck analysis has started"
python3.10 -m cppcheck temp/sources/cpp results
echo "Cppcheck analysis has finished"

# SpotBugs analysis
curl -L -o spotbugs-4.7.0.tgz "https://github.com/spotbugs/spotbugs/releases/download/4.7.0/spotbugs-4.7.0.tgz"
gunzip -c spotbugs-4.7.0.tgz | tar xvf -
echo "SpotBugs analysis has started"
python3.10 -m spotbugs spotbugs-4.7.0/lib/spotbugs.jar temp/sources/java results
echo "SpotBugs analysis has finished"

# Analyze reports and generate report
echo "Report generation has started"
python3.10 -m analyze_reports true

# get PDF report from .tex
echo "Conversion to PDF has started"
cd results/report
curl -L -o IEEEtran.cls "https://www.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/IEEEtran.cls"
tlmgr install href-ul ffcode totpages acmart hyperxmp ifmtarg ncctools preprint cleveref paralist comment biblatex needspace environ framed xstring catchfile fvextra libertine inconsolata newtx
latexmk report -pdf -shell-escape -f -quiet
rm -rf *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.run.xml *.out *.exc *.pyg _minted-report

