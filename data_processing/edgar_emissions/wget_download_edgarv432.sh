#!/bin/bash
# -------------------------------------------------------------------
# Script to download .nc edgar v4.3.2 2012 files using wget
# Run bash script from terminal. 
# Check script is executable: chmod +x wget_download_edgarv432.sh
# Check wget is installed
# -------------------------------------------------------------------
# Author: Eric Saboya, Department of Physics, Imperial College London
# Contact: ericsaboya54[at]gmail.com
# -------------------------------------------------------------------

# ****  Methane files ****
# Directory to download files to (spat-ocean)
DESTDIR="//home/ess17/Data/EmissionsInventories/EDGAR/v432/CH4/"

# EDGAR sector abbreviations
declare -a edgar_sector=("AGS" "AWB" "CHE" "ENE" "ENF" "FFF" "IND" "IRO" "MNM" "PRO" "RCO" "REF_TRF" "SWD_INC" "SWD_LDF" "TNR_Aviation_CDS" 
"TNR_Aviation_CRS" "TNR_Aviation_LTO" "TNR_Other" "TNR_Ship" "TRO" "WWT")

# IPCC EDGAR sector codes
declare -a ipcc_codes=("4C_4D1_4D2_4D4" "4F" "2B" "1A1a" "4A" "7A" "1A2" "2C1a_2C1c_2C1d_2C1e_2C1f_2C2" "4B" "1B1a_1B2a1_1B2a2_1B2a3_1B2a4_1B2c"
"1A4" "1A1b_1A1c_1A5b1_1B1b_1B2a5_1B2a6_1B2b5_2C1b" "6C" "6A_6D" "1A3a_CDS" "1A3a_CRS" "1A3a_LTO" "1A3c_1A3e" "1A3d_1C2" "1A3b" "6B")

# Number of EDGAR source sectors
len=${#edgar_sector[@]}
end=$((len - 1))

echo "Downloading EDGAR v4.3.2 *2012* CH4 emissions ..."

for i in $(seq 0 $end)
do
  echo "${edgar_sector[i]}"
  wget --no-check-certificate -P $DESTDIR "https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v432/CH4/${edgar_sector[i]}/v432_CH4_2012_IPCC_${ipcc_codes[i]}.0.1x0.1.zip"
done

