import schedule
import time
import csv
import os
import yfinance as yf
from datetime import date
from datetime import datetime
from function import preprocess_data, calculate_heiken_ashi, calculate_modified_heiken_ashi, calculate_EBL, calculate_EBR
from function import calculate_BTRG, calculate_STRG, calculate_historical_prices, calculate_buy
from function import calculate_stop_loss, calculate_sell, sell_stop_loss, calculate_targets

def preprocess_stock(stock, folder):
    ticker = yf.Ticker(stock)
    company_name = ticker.info.get('longName', stock)
    # Load stock data from Yahoo Finance
    data = yf.download(stock, start="2023-01-01",
                       end=date.today().strftime('%Y-%m-%d'))
    # If no data found, skip the stock and move to next stock
    if data.empty:
        print(f"{stock} skipped due to no data found")
        return
    # Apply the functions to preprocess the data
    preprocess_data(data)
    data = calculate_heiken_ashi(data)
    data = calculate_modified_heiken_ashi(data)
    data = calculate_EBR(data)
    data = calculate_EBL(data)
    data = calculate_BTRG(data)
    data = calculate_STRG(data)
    data = calculate_historical_prices(data)
    data = calculate_buy(data)
    data = calculate_sell(data)
    data = calculate_targets(data)
    data = calculate_stop_loss(data)
    data = sell_stop_loss(data)
    # Save the preprocessed data for the stock to a file
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{company_name}_{stock}.csv"
    filename = os.path.join(folder, filename)
    data.to_csv(filename)

def run_nifty_50():
    NSE_STOCKS = ["TCS.NS","RELIANCE.NS", "HDFCBANK.NS" , "ICICIBANK.NS","HINDUNILVR.NS", "INFY.NS", "HDFC.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS", "LIC.NS",
                 "LT.NS", "HCLTECH.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "DMART.NS", "ULTRACEMCO.NS", "BAJAJFINSV.NS", "WIPRO.NS", "ADANIENT.NS", "ONGC.NS", "NTPC.NS", "JSWSTEEL.NS", "POWERGRID.NS", "M&M.NS", "LTIM.NS", "TATAMOTORS.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "COALINDIA.NS", "TATASTEEL.NS", "HINDZINC.NS", "PIDILITIND.NS", "SIEMENS.NS", "ADANITRANS.NS", "SBILIFE.NS", "IOC.NS", "BAJAJ-AUTO.NS", "GRASIM.NS", "TECHM.NS", "HDFCLIFE.NS", "BRITANNIA.NS", "VEDL.NS", "GODREJCP.NS", "DABUR.NS", "ATGL.NS", "SHREECEM.NS", "HAL.NS", "HINDALCO.NS", "VBL.NS", "DLF.NS", "BANKBARODA.NS", "INDUSINDBK.NS", "EICHERMOT.NS", "DRREDDY.NS", "DIVISLAB.NS", "BPCL.NS", "HAVELLS.NS", "ADANIPOWER.NS", "INDIGO.NS", "CIPLA.NS", "AMBUJACEM.NS", "SRF.NS", "ABB.NS", "BEL.NS", "SBICARD.NS", "GAIL.NS", "BAJAJHLDNG.NS", "TATACONSUM.NS", "ICICIPRULI.NS", "CHOLAFIN.NS", "MARICO.NS", "APOLLOHOSP.NS", "TATAPOWER.NS", "BOSCHLTD.NS", "BERGEPAINT.NS", "JINDALSTEL.NS", "MCDOWELL-N.NS", "UPL.NS", "AWL.NS", "ICICIGI.NS", "TORNTPHARM.NS", "CANBK.NS", "PNB.NS", "TVSMOTOR.NS", "ZYDUSLIFE.NS", "TIINDIA.NS", "TRENT.NS", "IDBI.NS", "NAUKRI.NS", "SHRIRAMFIN.N", "HEROMOTOCO.NS", "INDHOTEL.NS", "PIIND.NS", "IRCTC.NS", "CGPOWER.NS", "UNIONBANK.NS", "MOTHERSON.NS", "CUMMINSIND.NS", "SCHAEFFLER.NS", "LODHA.NS", "ZOMATO.NS", "PGHH.NS", "YESBANK.NS", "POLYCAB.NS", "MAXHEALTH.NS", "IOB.NS", "PAGEIND.NS", "COLPAL.NS", "ASHOKLEY.NS", "ALKEM.NS", "NHPC.NS", "PAYTM.NS", "PFC.NS", "JSWENERGY.NS", "MUTHOOTFIN.NS", "AUBANK.NS", "INDUSTOWER.NS", "BALKRISIND.NS", "UBL.NS", "ABCAPITAL.NS", "TATAELXSI.NS", "DALBHARAT.NS", "HDFCAMC.NS", "INDIANB.NS", "ASTRAL.NS", "BHARATFORG.NS", "LTTS.NS", "MRF.NS", "TATACOMM.NS", "NYKAA.NS", "CONCOR.NS", "PERSISTENT.NS", "PATANJALI.NS", "IRFC.NS", "LINDEINDIA.NS", "IDFCFIRSTB.NS", "PETRONET.NS", "SOLARINDS.NS", "SAIL.NS", "MPHASIS.NS", "HINDPETRO.NS", "APLAPOLLO.NS", "FLUOROCHEM.NS", "NMDC.NS", "HONAUT.NS", "SUPREMEIND.NS", "GUJGASLTD.NS", "BANDHANBNK.NS", "ACC.NS", "OBEROIRLTY.NS", "BANKINDIA.NS", "RECLTD.NS", "AUROPHARMA.NS", "STAR.NS", "IGL.NS", "LUPIN.NS", "UCOBANK.NS", "JUBLFOOD.NS", "POLYPLEX.NS", "GODREJPROP.NS", "M&MFIN.NS", "IDEA.NS", "OFSS.NS", "FEDERALBNK.NS", "MANYAM.NS", "UNOMINDA.NS", "AIAENG.NS", "THERMAX.NS", "OIL.NS", "VOLTAS.NS", "3MINDIA.NS", "COROMANDEL.NS", "SUNDARMFIN.NS", "KPITTECH.NS", "DEEPAKNTR.NS", "ESCORTS.NS", "BIOCON.NS", "TATACHEM.NS", "TORNTPOWER.NS", "GMRINFRA.NS", "BHEL.NS", "SONACOMS.NS", "DELHIVERY.NS", "SYNGENE.NS", "CRISIL.NS", "GICRE.NS", "COFORGE.NS", "PHOENIXLTD.NS", "JKCEMENT.NS", "POONAWALLA.NS", "GLAXO.NS", "MFSL.NS", "METROPOLIS.NS", "MSUMI.NS", "SUMICHEM.NS", "RELAXO.NS", "NAVINFLUOR.NS", "SKFINDIA.NS", "CENTRALBK.NS", "GLAND.NS", "KANSAINER.NS", "GRINDWELL.NS", "TIMKEN.NS", "IPCALAB.NS", "SUNDRMFAST.NS", "ATUL.NS", "ZEEL.NS", "L&TFH.NS", "ABFRL.NS", "APOLLOTYRE.NS", "KPRMILL.NS", "ZFVCF.NS", "FORTIS.NS", "AARTIIND.NS", "HATSUN.NS", "CARBORUNIV.NS", "CROMPTON.NS", "VINATIORGA.NS", "IIFL.NS", "BATAINDIA.NS", "BDL.NS", "LICHSGFIN.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "ENDURANCE.NS", "DEVYANI.NS", "PSB.NS", "DIXON.NS", "KAJARIACER.NS", "WHIRLPOOL.NS", "MAHABANK.NS", "SUNTV.NS", "PEL.NS", "PRESTIGE.NS", "NIACL.NS", "RADICO.NS", "PFIZER.NS", "NH.NS", "EMAMILTD.NS", "LAURUSLABS.NS", "FIVESTAR.NS", "AJANTPHARM.NS", "INDIAMART.NS", "360ONE.NS", "KEI.NS", "JBCHEPHARM.NS", "LALPATHLAB.NS", "JSL.NS", "IRB.NS", "EXIDEIND.NS", "PVR.NS", "GSPL.NS", "BLUEDART.NS", "NATIONALUM.NS", "RVNL.NS", "CREDITACC.NS", "TRIDENT.NS", "POWERINDIA.NS", "MEDANTA.NS", "GILLETTE.NS", "RATNAMANI.NS", "ELGIEQUIP.NS", "ISEC.NS", "CGCL.NS", "GODREJIND.NS", "CLEAN.NS", "MAZDOCK.NS", "MAHINDCIE.NS", "AEGISCHEM.NS", "FACT.NS", "BLUESTARCO.NS", "SANOFI.NS", "FINEORG.NS", "AFFLE.NS", "GLENMARK.NS", "NAM-INDIA.NS", "SJVN.NS", "REDINGTON.NS", "AAVAS.NS", "IDFC.NS", "FINCABLES.NS", "NUVOCO.NS", "BAJAJELEC.NS", "APTUS.NS", "SUVENPHAR.NS", "ASTERDM.NS", "RHIM.NS", "KEC.NS", "SONATSOFTW.NS", "AETHER.NS", "DCMSHRIRAM.NS", "IEX.NS", "HAPPSTMNDS.NS", "KIMS.NS", "ALKYLAMINE.NS", "CYIENT.NS", "CHAMBLFERT.NS", "ASAHIINDIA.NS", "CASTROLIND.NS", "BRIGADE.NS", "KALYANKJIL.NS", "TTML.NS", "VGUARD.NS", "NLCINDIA.NS", "LAXMIMACH.NS", "TRITURBINE.NS", "FINPIPE.NS", "AKZOINDIA.NS", "MANAPPURAM.NS", "EIHOTEL.NS", "CENTURYPLY.NS", "NATCOPHARM.NS", "KIOCL.NS", "CHOLAHLDNG.NS", "CAMPUS.NS", "CAMS.NS", "AMARAJABAT.NS", "ZYDUSWELL.NS", "BASF.NS", "TEJASNET.NS", "APLLTD.NS", "MGL.NS", "GRINFRA.NS", "ANGELONE.NS", "SFL.NS", "TTKPRESTIG.NS", "APARINDS.NS", "HINDCOPPER.NS", "CDSL.NS", "GODFRYPHLP.NS", "RENUKA.NS", "CITYUNIONBANK.NS", "JKLAKSHMI.NS", "ANURAS.NS", "MRPL.NS", "GESHIP.NS", "POLYMED.NS", "NSNLNISP.NS", "BIKAJI.NS", "MOTILALOFS.NS", "ABSLAMC.NS", "CESC.NS", "TATAINVEST.NS", "ALLCARGO.NS", "KALPATPOWR.NS", "PNBHOUSING.NS", "HUDCO.NS", "ITI.NS", "ROUTE.NS", "RITES.NS", "VTL.NS", "RBLBANK.NS", "HFCL.NS", "KARURVYSYA.NS", "CERA.NS", "EIDPARRY.NS", "INGERRAND.NS", "GALAXYSURF.NS", "PPL.NS", "UTIAMC.NS", "KRBL.NS", "RAYMOND.NS", "ASTRAZEN.NS", "VIPIND.NS", "SUZLON.NS", "GODREJAGRO.NS", "GNFC.NS", "ERIS.NS", "PGHL.NS", "MEDPLUS.NS", "SAPPHIRE.NS", "DATAPATT.NS", "UNCLAYLTD.NS", "JBMA.NS", "EASEMYTRIP.NS", "CCL.NS", "EQUITASBNK.NS", "CHALET.NS", "RAINBOW.NS", "PNCINFRA.NS", "FSL.NS", "KSB.NS", "BSOFTEC.NS", "KNRCON.NS", "SHOPERSTOP.NS", "SYMPHONY.NS", "CENTURYTEX.NS", "CANFINHOME.NS", "GRANULES.NS", "TANLA.NS", "JYOTHYLAB.NS", "SPLIL.NS", "DEEPAKFERT.NS", "CRAFTSMAN.NS", "BIRLACORPN.NS", "BLS.NS", "SHYAMMETL.NS", "NCC.NS", "GMMPFAUDLR.NS", "LATENTVIEW.NS", "USHAMART.NS", "HOMEFIRST.NS", "JKPAPER.NS", "TMBANK.NS", "JINDWORLD.NS", "METROPOLIS.NS", "SAREGAMA.NS", "NBCC.NS", "ECLERX.NS", "BALAMINES.NS", "WELSPUNIND.NS", "PRAJIND.NS", "COCHINSHIP.NS", "ZENSARTECH.NS", "AMBER.NS", "LEMONTREE.NS", "PRINCEPIPE.NS", "TRIVENI.NS", "GARFIBRES.NS", "LXCHEM.NS", "STLTECH.NS", "CEATLTD.NS", "BSE.NS", "SPARC.NS", "ALOKINDS.NS", "ORIENTELEC.NS", "INDIACEM.NS", "JUBLINGREA.NS", "KIRLOSENG.NS", "TCIEXP.NS", "JMFINANCIL.NS", "NETWORK18.NS", "SWANENERGY.NS", "GPPL.NS", "KAYNES.NS", "VRLLOG.NS", "INTELLECT.NS", "SWSOLAR.NS", "CHEMPLASTS.NS", "QUESS.NS", "ROLEXRINGS.NS", "MAHLIFE.NS", "ESABINDIA.NS", "MHRIL.NS", "GOCORAL.NS", "HGS.NS", "BORORENEW.BO", "GAEL.NS", "MAPMYIND.BO", "PRSMJOHNSN.NS", "RUSTOMJEE.NS", "IRCON.NS", "RCF.NS", "WELCORP.NS", "BEML.NS", "GRSE.NS", "EPL.NS", "MINDACORP.NS", "GRAPHITE.NS", "HGINFRA.NS", "OLECTRA.NS", "RELINFRA.NS", "JUSTDIAL.NS", "RAIN.NS", "IONEXCHANG.NS", "EDELWEISS.NS", "UJJIVANSFB.NS", "TV18BRDCST.NS", "GPIL.NS", "MTAR.NS", "TCI.NS", "RTNINDIA.NS", "VSTIND.NS", "SAFARI.NS", "ACE.NS",
                    "MAHSCOOTER.NS","DELTACORP.NS", "GLS.NS", "GHCL.NS", "INDIGOPNTS.NS", "MAHSEAMLES.NS", "SUPRAJIT.BO", "KFINT.BO", "GSFC.NS", "J&KBANK.NS", "RELIGARE.BO", "MASTEK.NS", "SIS.NS", "JINDALSAW.NS", "TEGAIN.NS", "SYRMA.NS", "AVANTIFEED.NS", "STARCEMENT.NS", "IBULHSGFIN.NS", "RKFORGE.NS", "CAPLIPOINT.NS", "VAIBHAVGBL.NS", "RBL.NS", "JUBLPHARMA.NS", "SHARDACROP.NS", "NIITLTD.NS", "PCBL.NS", "MASFIN.NS", "SHIPPING.NS", "PDSM.NS", "GUJALKALI.NS", "ELECON.NS", "CMSLTD.NS", "VMART.NS", "ICRA.NS", "JSWHL.NS", "FDC.NS", "CSBBANK.NS", "KTKBANK.NS", "MMTC.NS", "ENGINERSIN.NS", "SUNTECK.NS", "PRIVISCL.NS", "PARADEEP.NS", "SOBHA.NS", "FUSION.NS", "GMDCLTD.NS", "VIJAYABANK.NS", "JAMNAAUTO.NS", "ANANTRAJ.NS", "SANSERA.NS", "MFL.NS", "AHLUCONT.NS", "BSHSL.NS", "TATACOFFEE.NS", "TEAMLEASE.NS", "JKTYRE.NS", "VARROC.NS", "GREENLAM.NS", "JPPOWER.NS", "INFIBEAM.NS", "SPANDANA.NS", "HSCL.NS", "BHARATRAS.NS", "RAJRATAN.NS", "LAOPALA.NS", "SARDAEN.NS", "RALLIS.NS", "BORORENEW.NS", "RATEGAIN.NS", "SCHNEIDER.NS", "RPWR.BO", "ARVINDFASN.NS", "TATVA.NS", "POWERMECH.NS", "HCG.NS", "NESCO.NS", "HEIDELBERG.NS", "TECHNOE.BO", "POLYPLEX.BO", "SURYAROSNI.NS", "AUTOAXLES.NS", "JWIL.NS", "NFL.NS", "HEG.NS", "RAJRATAN.NS", "CHENNPETRO.NS", "WESTCOASTP.NS", "LUXIND.NS", "HIKAL.NS", "MIDHANI.NS", "HLEGLAS.NS", "SHAREINDIA.NS", "NOCIL.NS", "NAZARA.NS", "BANARISUG.NS", "ANANDRATHI.NS", "PRUDENT.NS", "GRAVITA.NS", "GREENPANEL.NS", "VESUVIUS.NS", "DCBBANK.NS", "ROSSARI.NS", "RESPONIND.NS", "TINPLATE.NS", "KIRLOSBROS.NS", "RAILTEL.NS", "AMIORG.NS", "ISGEC.NS", "NEOGEN.NS", "MARKSANS.NS", "NAVA.NS", "NEWGEN.NS", "BECTORFOOD.NS", "TWL.NS", "AARTIDRUGS.NS", "UJJIVAN.NS", "GATEWAY.NS", "SULA.NS", "DAAWAT.NS", "SOUTHBANK.NS", "GET&D.NS", "HARSHA.NS", "PGEL.NS", "RSYSTEMS.NS", "INDOCO.NS", "MOLDTKPAC.NS", "IFBIND.NS", "SBCL.NS", "BCG.NS", "GREAVESCOT.NS", "MOIL.NS", "TATASTLLP.NS", "TARSONS.NS", "SHANTIGEAR.NS", "CHOICEIN.NS", "TIIL.NS", "DHANUKA.NS", "JCHAC.NS", "DODLA.NS", "DALMIASUG.NS", "VOLTAMP.NS", "ASTEC.NS", "SUDARSCHEM.NS", "KSCL.NS", "SUNFLAG.NS", "IBREALEST.NS", "THOMASCOOK.NS", "HBLPOWER.NS", "INOXWIND.NS", "NILKAMAL.NS", "ZENTEC.NS", "TCNSBRANDS.NS", "ADVENZYMES.NS", "STAR.NS", "FCL.NS", "KKCL.NS", "HINDWAREAP.NS", "MAHLOG.NS", "EMIL.NS", "JTEKTINDIA.NS", "MANINFRA.NS", "ITDC.NS", "APCOTEXIND.NS", "PRICOLLTD.NS", "PTC.NS", "AARTIPHARM.NS", "MBAPL.NS", "SAGCEM.NS", "TDPOWERSYS.NS", "JAICORPLTD.NS", "DBL.NS", "BARBEQUE.NS", "UNIPARTS.NS", "UFLEX.NS", "WONDERLA.NS", "PSPPROJECT.NS", "KIRLOSIND.NS", "IPL.NS", "DISHTV.NS", "TATAMETALI.NS", "PAISALO.NS", "PFOCUS.NS", "HEMIPROP.NS", "LGBBROSLTD.NS", "MAITHANALL.NS", "SSWL.NS", "NEULANDLAB.NS", "HATHWAY.NS", "THYROCARE.NS", "ORIENTCEM.NS", "DREAMFOLKS.NS", "ETHOSLTD.NS", "GLOBUSSPR.NS", "GANESHHOUC.NS", "ARVIND.NS", "ICIL.NS", "SHRIPISTON.NS", "WOCKPHARMA.NS", "DBREALTY.NS", "ISMTLTD.NS", "JINDALPOLY.NS", "WABAG.NS", "BAJAJCON.NS", "GENUSPOWER.NS", "BUTTERFLY.NS", "NAVNETEDUL.NS", "GOKEX.NS", "APOLLOPIPE.NS", "LANDMARK.NS", "IFCI.NS", "ATFL.NS", "EVEREADY.NS", "AGI.NS", "TI.NS", "ASHOKA.NS", "SOMANYCERA.NS", "HCC.NS", "JISLJALEQS.NS", "VINDHYATEL.NS", "FIEMIND.NS", "TASTYBITE.NS", "JAYNECOIND.NS", "HONDAPOWER.NS", "UNICHEMLAB.NS", "MUKANDLTD.NS", "CIGNITITEC.NS", "MMFL.NS", "VENKEYS.NS", "RAMKY.NS", "DIVGIITTS.NS", "CAMLINFINE.NS", "SHILPAMED.NS", "GULFOILLUB.NS", "MOL.NS", "DOLLAR.NS", "VSTTILLERS.NS", "SUBROS.NS", "DCAL.NS", "GABRIEL.NS", "MAXVIL.NS", "SIYSIL.NS", "TVSSRICHAK.NS", "ASTRAMICRO.NS", "JKIL.NS", "JAGRAN.NS", "ELECTCAST.NS", "CARERATING.NS", "INDIAGLYCO.NS", "BALMLAWRIE.NS", "KOLTEPATIL.NS", "IMAGICAA.NS", "WELENT.NS", "TIPSINDLTD.NS", "SWARAJENG.NS", "MAYURUNIQ.NS", "GANECOS.NS", "PARAS.NS", "LUMAXTECH.NS", "ACCELYA.NS", "KESORAMIND.NS", "CARTRADE.NS", "MPSLTD.NS", "SEQUENT.NS", "HIL.NS", "GUFICBIO.NS", "ITDCEM.NS", "PILANIINVS.NS", "MSTCLTD.NS", "LSIL.NS", "PANAMAPET.NS", "OPTIEMUS.NS", "SIRCA.NS", "TIRUMALCHM.NS", "DYNAMATECH.NS", "SUNDARMHLD.NS", "TIMETECHNO.NS", "DBCORP.NS", "ASHIANA.NS", "CONFIPET.NS", "DIAMONDYD.NS", "NUCLEUS.NS", "GREENPLY.NS", "JPASSOCIAT.NS", "WENDT.NS", "FINOPB.NS", "FMGOETZE.NS", "SANGHIIND.NS", "VAKRANGEE.NS", "GNA.NS", "AMRUTANJAN.NS", "EMUDHRA.NS", "DATAMATICS.NS", "SHARDAMOTR.NS", "IOLCP.NS", "LUMAXIND.NS", "BAJAJHIND.NS", "STYLAMIND.NS", "ANDHRAPAP.NS", "SOTL.NS", "ADFFOODS.NS", "VIDHIING.NS", "KABRAEXTRU.NS", "BEPL.NS", "RUPA.NS", "NACLIND.NS", "VSSL.NS", "VISHNU.NS", "DWARKESH.NS", "DHANI.NS", "BANCOINDIA.NS", "KINGFA.NS", "SUBEXLTD.NS", "HINDOILEXP.NS", "RTNPOWER.NS", "VADILALIND.NS", "BBOX.NS", "ORCHPHARMA.NS", "PURVA.NS", "COSMOFIRST.NS", "IMFA.NS", "SUPRIYA.NS", "SAKSOFT.NS", "IIFLSEC.NS", "SANGHVIMOV.NS", "GOKULAGRO.NS", "ALEMBICLTD.NS", "VENUSPIPES.NS", "SEAMECLTD.NS", "TNPL.NS", "KPIGREEN.NS", "BFINVEST.NS", "SESHAPAPER.NS", "DHAMPURSUG.NS", "ANDHRSUGAR.NS", "KIRIINDUS.NS", "TTKHLTCARE.NS", "CARYSIL.NS", "GOCLCORP.NS", "JSWISPL.NS", "STERTOOLS.NS", "SHALBY.NS", "TIDEWATER.NS", "KRSNAA.NS", "KRISHANA.NS", "HUHTAMAKI.NS", "BBL.NS", "SEPC.NS", "ORISSAMINE.NS", "FILATEX.NS", "THEJO.NS", "APTECHT.NS", "ORIENTHOT.NS", "DCXINDIA.NS", "FOSECOIND.NS", "GOLDIAM.NS", "SHANKARA.NS", "INSECTICID.NS", "THANGAMAYL.NS", "SHK.NS", "TEXRAIL.NS", "CANTABIL.NS", "GALLANTT.NS", "HERITGFOOD.NS", "KCP.NS", "MOREPENLAB.NS", "GATI.NS", "RAMASTEEL.NS", "HESTERBIO.NS", "NRBBEARING.NS", "INDOSTAR.NS", "MONTECARLO.NS", "KSL.NS", "KDDL.NS", "TCPLPACK.NS", "MARATHON.NS", "ARVSMART.NS", "DCW.NS", "DEN.NS", "STEELXIND.NS", "EIHAHOTELS.NS", "IGPL.NS", "NITINSPIN.NS", "EXPLEOSOL.NS", "VERANDA.NS", "SALASAR.NS", "STYRENIX.NS", "ADORWELD.NS", "BHAGCHEM.NS", "PCJEWELLER.NS", "GENESYS.NS", "STOVEKRAFT.NS", "RANEHOLDIN.NS", "NDTV.NS", "XPROINDIA.NS", "MANORAMA.NS", "GRWRHITECH.NS", "HARIOMPIPE.NS", "SANDHAR.NS", "AVTNPL.NS", "IWEL.NS", "SJS.NS", "EVERESTIND.NS", "FAIRCHEMOR.NS", "SASKEN.NS", "OAL.NS", "NELCO.NS", "RIIL.NS", "SOLARA.NS", "TAJGVK.NS", "BOMDYEING.NS", "MANGCHEFER.NS", "GOODLUCK.NS", "RPGLIFE.NS", "PATELENG.NS", "SPIC.NS", "INOXGREEN.NS", "GIPCL.NS", "UNIVCABLES.NS", "NSIL.NS", "HMT.NS", "MATRIMONY.NS", "MTNL.NS", "SDBL.NS", "VALIANTORG.NS", "ARMANFIN.NS", "REPCOHOME.NS", "HERANBA.NS", "BFUTILITIE.NS", "PRECWIRE.NS", "AXITA.NS", "GRMOVER.NS", "GTPL.NS", "IGARASHI.NS", "INFOBEAN.NS", "ALICON.NS", "THEMISMED.NS", "TVTODAY.NS", "WHEELS.NS", "RPSGVENT.NS", "RAMCOIND.NS", "SMLISUZU.NS", "AHL.NS", "UNIENTER.NS", "SATIN.NS", "KUANTUM.NS", "GANESHBE.NS", "SUVEN.NS", "SATIA.NS", "GULPOLY.NS", "UGARSUGAR.NS", "MANALIPETC.NS", "PIXTRANS.NS", "SHRIRAMPPS.NS", "RADIANTCMS.NS", "PNBGILTS.NS", "INDORAMA.NS", "ASHAPURMIN.NS", "UGROCAP.NS", "AXISCADES.NS", "HITECH.NS", "PUNJABCHEM.NS", "SURYODAY.NS", "EKC.NS", "JASH.NS", "DPSCLTD.NS", "TARC.NS", "BHARATWIRE.NS", "EXCELINDUS.NS", "SPECIALITY.NS", "ANUP.NS", "SKIPPER.NS", "AJMERA.NS", "SHALPAINTS.NS", "GMBREW.NS", "SANGAMIND.NS", "SHIVALIK.NS", "GMRP&UI.NS", "PENIND.NS", "GEOJITFSL.NS", "BCLIND.NS", "DBOL.NS", "SHAILY.NS", "LIKHITHA.NS", "MADRASFERT.NS", "STEELCAS.NS", "MKPL.NS", "ROSSELLIND.NS",
                   "BPL.NS", "BIRLAMONEY.NS", "GPTINFRA.NS", "E2E.NS", "SHIVAMAUTO.NS", "DCMNVL.NS", "MAZDA.NS", "MADHAVBAUG.NS", "WINDMACHIN.NS", "BASML.NS", "WALCHANNAG.NS", "SEJALLTD.NS", "UCALFUEL.NS", "MAHEPC.NS", "V2RETAIL.NS", "SAKUMA.NS", "VERTOZ.NS", "KMSUGAR.NS", "ASHIMASYN.NS", "UFO.NS", "VIKASECO.NS", "SAKHTISUG.NS", "MAHESHWARI.NS", "MAANALU.NS", "HUBTOWN.NS", "REPL.NS", "QMSMEDI.NS", "MANAKSTEEL.NS", "EMAMIREAL.NS", "GENCON.NS", "STARPAPER.NS", "GUJAPOLLO.NS", "JAYSREETEA.NS", "NDL.NS", "BCONCEPTS.NS", "GIRRESORTS.NS", "SMLT.NS", "TPLPLASTEH.NS", "TEMBO.NS", "DANGEE.NS", "NIPPOBATRY.NS", "ASIANHOTNR.NS", "BRNL.NS", "PPAP.NS", "PASUPTAC.NS", "FROG.NS", "ASAHISONG.NS", "PRECOT.NS", "MEP.NS", "VENUSREM.NS", "KILITCH.NS", "BTML.NS", "MEGASTAR.NS", "DRCSYSTEMS.NS", "ZODIACLOTH.NS", "HILTON.NS", "INDOTHAI.NS", "JITFINFRA.NS", "EROSMEDIA.NS", "DEVIT.NS", "BIL.NS", "EIMCOELECO.NS", "ANMOL.NS", "COASTCORP.NS", "RAJTV.NS", "KORE.NS", "RELCAPITAL.NS", "MGEL.NS", "FOCE.NS", "INDTERRAIN.NS", "TAKE.NS", "TOTAL.NS", "ACCURACY.NS", "AVG.NS", "HARRMALAYA.NS", "SHREYANIND.NS", "LOKESHMACH.NS", "LGBFORGE.NS", "SYSTANGO.NS", "SIGMA.NS", "MARALOVER.NS", "ABAN.NS", "BAFNAPH.NS", "BEDMUTHA.NS", "SIMPLEXINF.NS", "ARIES.NS", "DTIL.NS", "KRITINUT.NS", "IVC.NS", "IITL.NS", "SWASTIK.NS", "AARON.NS", "VITAL.NS", "BEWLTD.NS", "NILAINFRA.NS", "INDOTECH.NS", "PVP.NS", "AHLEAST.NS", "SAH.NS", "TIPSFILMS.NS", "PHANTOMFX.NS", "DUCOL.NS", "KANPRPLA.NS", "VINNY.NS", "MCLEODRUSS.NS", "TRF.NS", "ALLETEC.NS", "MANOMAY.NS", "INSPIRISYS.NS", "AIRAN.NS", "MODISONLTD.NS", "MURUDCERA.NS", "TIRUPATI.NS", "PAR.NS", "SGIL.NS", "SPLIL.NS", "GEEKAYWIRE.NS", "PALREDTEC.NS", "ESSARSHPNG.NS", "SIL.NS", "PRITI.NS", "AKSHARCHEM.NS", "RAMANEWS.NS", "RUCHINFRA.NS", "ALANKIT.NS", "MEGASOFT.NS", "IZMO.NS", "GULFPETRO.NS", "TOUCHWOOD.NS", "SARVESHWAR.NS", "TARMAT.NS", "RPPL.NS", "IEL.NS", "BHARATGEAR.NS", "GOLDTECH.NS", "MBLINFRA.NS", "PROPEQUITY.NS", "EMKAY.NS", "IL&FSENGG.NS", "BSL.NS", "UNITEDPOLY.NS", "PASHUPATI.NS", "SHIVATEX.NS", "MANGALAM.NS", "KRISHNADEF.NS", "PREMIERPOL.NS", "SMSLIFE.NS", "GOLDSTAR.NS", "BROOKS.NS", "VAISHALI.NS", "ALMONDZ.NS", "3RDROCK.NS", "PRESSMN.NS", "AARVI.NS", "AKSHAR.NS", "LATTEYS.NS", "VISESHINFO.NS", "BHAGYANGR.NS", "TTL.NS", "SADBHAV.NS", "COMPUSOFT.NS", "KAKATCEM.NS", "RPPINFRA.NS", "SVLL.NS", "SMARTLINK.NS", "ASPINWALL.NS", "LAMBODHARA.NS", "DJML.NS", "TIL.NS", "ELGIRUBCO.NS", "JAINAM.NS", "WORTH.NS", "ISFT.NS", "GINNIFILA.NS", "PILITA.NS", "SOFTTECH.NS", "DUCON.NS", "VETO.NS", "RANEENGINE.NS", "AVONMORE.NS", "KBCGLOBAL.NS", "PANSARI.NS", "MODIRUBBER.NS", "INVENTURE.NS", "KAPSTON.NS", "AKSHOPTFBR.NS", "JMA.NS", "EMMBI.NS", "NITCO.NS", "IRIS.NS", "SHERA.NS", "DRSDILIP.NS", "UNITEDTEA.NS", "JOCIL.NS", "MANAKALUCO.NS", "VIPULLTD.NS", "SIKKO.NS", "GILLANDERS.NS", "SVPGLOB.NS", "VISASTEEL.NS", "DCM.NS", "INTENTECH.NS", "TEXMOPIPES.NS", "WEIZMANIND.NS", "BYKE.NS", "RAJSREESUG.NS", "ZODIAC.NS", "ARSHIYA.NS", "UMANGDAIRY.NS", "LOVABLE.NS", "HOMESFY.NS", "ALPHAGEO.NS", "NDGL.NS", "PRAXIS.NS", "ARTNIRMAN.NS", "SHIGAN.NS", "NOIDATOLL.NS", "UMAEXPORTS.NS", "VELS.NS", "ATLANTA.NS", "MOTOGENFIN.NS", "AVROIND.NS", "SALONA.NS", "INDIANCARD.NS", "SPTL.NS", "PRITIKAUTO.NS", "URAVI.NS", "IVP.NS", "MAHAPEXLTD.NS", "SOMATEX.NS", "LEXUS.NS", "WANBURY.NS", "LOTUSEYE.NS", "KREBSBIO.NS", "RNAVAL.NS", "WSI.NS", "RHFL.NS", "HDIL.NS", "DCI.NS", "RVHL.NS", "XELPMOC.NS", "RKEC.NS", "RELCHEMQ.NS", "DIL.NS", "ATALREAL.NS", "KOHINOOR.NS", "SALSTEEL.NS", "A2ZINFRA.NS", "TARACHAND.NS", "INDOWIND.NS", "BLBLIMITED.NS", "FRETAIL.NS", "ROML.NS", "SURANAT&P.NS", "ALPA.NS", "SUNDRMBRAK.NS", "PARIN.NS", "NILASPACES.NS", "AHLADA.NS", "MAGNUM.NS", "REMSONSIND.NS", "STARTECK.NS", "BOHRAIND.NS", "COMPINFO.NS", "CORALFINAC.NS", "MRO-TEK.NS", "SECURKLOUD.NS", "ZEELEARN.NS", "SADBHIN.NS", "BALPHARMA.NS", "NIRAJ.NS", "GSTL.NS", "OBCL.NS", "TAINWALCHM.NS", "ARCHIDPLY.NS", "JHS.NS", "SITINET.NS", "MUKTAARTS.NS", "CMNL.NS", "GAYAPROJ.NS", "AKG.NS", "FCONSUMER.NS", "PALASHSECU.NS", "CCHHL.NS", "SIGIND.NS", "AIROLAM.NS", "WELINV.NS", "LEMERITE.NS", "CTE.NS", "UNIVASTU.NS", "SUNDARAM.NS",
                   "MANAKCOAT.NS", "ARVEE.NS", "SECURCRED.NS", "ASTRON.NS", "FLFL.NS", "STEELCITY.NS", "LLOYDS.NS", "GANGESSECU.NS", "INDBANK.NS", "SUMIT.NS", "FIBERWEB.NS", "ALKALI.NS", "LASA.NS", "JAIPURKURT.NS", "MHHL.NS", "BAHETI.NS", "DGCONTENT.NS", "VMARCIND.NS", "PKTEA.NS", "DAMODARIND.NS", "NECCLTD.NS", "CAPTRUST.NS", "MITCON.NS", "TIRUPATIFL.NS", "IL&FSTRANS.NS", "SRPL.NS", "SURYALAXMI.NS", "CEREBRAINT.NS", "KSHITIJPOL.NS", "LAGNAM.NS", "ANLON.NS", "AMJLAND.NS", "BINANIIND.NS", "PROLIFE.NS", "INCREDIBLE.NS", "SHAHALLOYS.NS", "AMDIND.NS", "OMAXAUTO.NS", "TOKYOPLAST.NS", "GROBTEA.NS", "ANIKINDS.NS", "SURANASOL.NS", "FIDEL.NS", "MAHASTEEL.NS", "AURDIS.NS", "SIMBHALS.NS", "GAL.NS", "GICL.NS", "KALYANIFRG.NS", "HINDCON.NS", "CORDSCABLE.NS", "YAARI.NS", "SONAMCLOCK.NS", "MAHICKRA.NS", "HPIL.NS", "LPDC.NS", "DBSTOCKBRO.NS", "AUSOMENT.NS", "BALLARPUR.NS", "AVSL.NS", "SPMLINFRA.NS", "BANKA.NS", "GOLDENTOBC.NS", "GTL.NS", "ENERGYDEV.NS", "PANACHE.NS", "PIGL.NS", "DELTAMAGNT.NS", "SHRADHA.NS", "PIONEEREMB.NS", "GLOBALVECT.NS", "BAGFILMS.NS", "WIPL.NS", "NITIRAJ.NS", "BEARDSELL.NS", "KRITIKA.NS", "PATINTLOG.NS", "SETCO.NS", "PRAENG.NS", "ELECTHERM.NS", "UCL.NS", "PRAKASHSTL.NS", "CINEVISTA.NS", "SUULD.NS", "FLEXITUFF.NS", "MDL.NS", "HISARMETAL.NS", "SUVIDHAA.NS", "BIOFILCHEM.NS", "MARSHALL.NS", "ARIHANTACA.NS", "CELEBRITY.NS", "VIAZ.NS", "DHRUV.NS", "CENTEXT.NS", "DOLLEX.NS", "BHANDARI.NS", "TREJHARA.NS", "FELIX.NS", "NGIL.NS", "SUPREMEINF.NS", "AGROPHOS.NS", "MCL.NS", "OILCOUNTUB.NS", "UMA.NS", "MORARJEE.NS", "SRIVASAVI.NS", "AAREYDRUGS.NS", "AAKASH.NS", "VASWANI.NS", "KANANIIND.NS", "ARCHIES.NS", "SHIVAMILLS.NS", "IPSL.NS", "TREEHOUSE.NS", "BDR.NS", "VERTEXPLUS.NS", "KEYFINSERV.NS", "KHFM.NS", "AROGRANITE.NS", "SEYAIND.NS", "GIRIRAJ.NS", "RSSOFTWARE.NS", "ORIENTLTD.NS", "EXCEL.NS", "RELIABLE.NS", "AAATECH.NS", "AGRITECH.NS", "LGHL.NS", "SHRENIK.NS", "ANKITMETAL.NS", "JETFREIGHT.NS", "VARDMNPOLY.NS", "NIRMAN.NS", "SHREERAMA.NS", "SIDDHIKA.NS", "BVCL.NS", "KKVAPOW.NS", "HOVS.NS", "AMBANIORG.NS", "FSC.NS", "ABMINTLLTD.NS", "SEPOWER.NS", "BANARBEADS.NS", "REGENCERAM.NS", "PODDARHOUS.NS", "PENTAGOLD.NS", "PARTYCRUS.NS", "SONAHISONA.NS", "MALUPAPER.NS", "MOKSH.NS", "PULZ.NS", "RBMINFRA.NS", "ZENITHSTL.NS", "NIDAN.NS", "SAMBHAAV.NS", "UWCSL.NS", "BANG.NS", "MRO.NS", "MINDPOOL.NS", "TAPIFRUIT.NS", "ABCOTS.NS", "PNC.NS", "SURANI.NS", "PRECISION.NS", "TIMESGTY.NS", "MANUGRAPH.NS", "ZENITHEXPO.NS", "AARVEEDEN.NS", "SOMICONVEY.NS", "DKEGL.NS", "ARHAM.NS", "TIMESCAN.NS", "SGL.NS", "WEWIN.NS", "CMRSL.NS", "SONUINFRA.NS", "VIVIANA.NS", "AKASH.NS", "INDSWFTLTD.NS", "KARMAENG.NS", "NAGREEKEXP.NS", "BURNPUR.NS", "NIBL.NS", "CUBEXTUB.NS", "AISL.NS", "SHAIVAL.NS", "VINEETLAB.NS", "ARISTO.NS", "TERASOFT.NS", "CROWN.NS", "JFLLIFE.NS", "GLOBE.NS", "3PLAND.NS", "VERA.NS", "MILTON.NS", "ADROITINFO.NS", "SHUBHLAXMI.NS", "AGNI.NS", "LFIC.NS", "VSCL.NS", "MADHAV.NS", "UJAAS.NS", "SUPERSPIN.NS", "RKDL.NS", "AMBICAAGAR.NS", "ACEINTEG.NS", "OMFURN.NS", "SWARAJ.NS", "AJOONI.NS", "KHANDSE.NS", "SAGARDEEP.NS", "REXPIPES.NS", "ADL.NS", "MCON.NS", "CADSYS.NS", "HBSL.NS", "SANGINITA.NS", "GANGAFORGE.NS", "ABINFRA.NS", "PERFECT.NS", "NARMADA.NS", "RMDRIP.NS", "NAGREEKCAP.NS", "LAXMICOT.NS", "PEARLPOLY.NS", "HECPROJECT.NS", "SANWARIA.NS", "MEGAFLEX.NS", "GISOLUTION.NS", "PARASPETRO.NS", "RITEZONE.NS", "HEADSUP.NS", "VCL.NS", "PRITIKA.NS", "KEEPLEARN.NS", "COUNCODOS.NS", "ROLTA.NS", "DHARSUGAR.NS", "ASLIND.NS", "AGARWALFT.NS", "NEXTMEDIA.NS", "RICHA.NS", "DNAMEDIA.NS", "AMEYA.NS", "DYNAMIC.NS", "LIBAS.NS", "JETKNIT.NS", "BALKRISHNA.NS", "MTEDUCARE.NS", "GODHA.NS", "GOENKA.NS", "HAVISHA.NS", "QUADPRO.NS", "QFIL.NS", "MADHUCON.NS", "ROLLT.NS", "CYBERMEDIA.NS", "JAKHARIA.NS", "VEEKAYEM.NS", "TGBHOTELS.NS", "VIVIDHA.NS", "FMNL.NS", "WALPAR.NS", "DESTINY.NS", "SUMEETINDS.NS", "ICDSLTD.NS", "LRRPL.NS", "MPTODAY.NS", "21STCENMGM.NS", "HYBRIDFIN.NS", "SABAR.NS", "TFL.NS", "IMPEXFERRO.NS", "INFOMEDIA.NS", "NKIND.NS", "SHANTI.NS", "GRCL.NS", "FEL.NS", "THOMASCOTT.NS", "KHAITANLTD.NS", "WILLAMAGOR.NS", "LCCINFOTEC.NS", "UNIINFO.NS", "ASMS.NS", "VIVO.NS", "GAYAHWS.NS", "CALSOFT.NS", "MOXSH.NS", "ORIENTALTL.NS", "ONELIFECAP.NS", "VIJIFIN.NS", "DIGJAMLMTD.NS", "KRIDHANINF.NS", "SILLYMONKS.NS", "MAKS.NS", "TANTIACONS.NS", "SUPREMEENG.NS", "SILGO.NS", "MOHITIND.NS", "EDUCOMP.NS", "EASTSILK.NS", "KANDARP.NS", "CMICABLES.NS", "NATNLSTEEL.NS", "MITTAL.NS", "SPRL.NS", "ORTINLAB.NS", "BRIGHT.NS", "KAUSHALYA.NS", "GUJRAFFIA.NS", "MASKINVEST.NS", "ISHAN.NS", "CONTI.NS", "AMIABLE.NS", "AILIMITED.NS", "EUROTEXIND.NS", "TIJARIA.NS", "TNTELE.NS", "KALYANI.NS", "SETUINFRA.NS", "GRETEX.NS", "LYPSAGEMS.NS", "METALFORGE.NS", "SSINFRA.NS", "SMVD.NS", "RMCL.NS", "JALAN.NS", "SANCO.NS", "VASA.NS", "KAVVERITEL.NS", "TECHIN.NS", "NORBTEAEXP.NS", "KCK.NS", "SPENTEX.NS", "CREATIVEYE.NS", "ANTGRAPHIC.NS", "TVVISION.NS", "ABNINT.NS", "ARENTERP.NS", "UMESLTD.NS", "SHYAMTEL.NS", "MANAV.NS", "ACCORD.NS", "DRL.NS", "GLFL.NS", "CMMIPL.NS", "NIRAJISPAT.NS", "DCMFINSERV.NS", "SRIRAM.NS", "PREMIER.NS", "SKSTEXTILE.NS", "SABTN.NS", "TARAPUR.NS", "BKMINDST.NS", "ALPSINDUS.NS", "AHIMSA.NS", "BHALCHANDR.NS", "INNOVATIVE.NS", "LAKPRE.NS", "TRANSWIND.NS", "MELSTAR.NS", "SABEVENTS.NS", "INDLMETER.NS", "TECILCHEM.NS", "ABHISHEK.NS", "AHLWEST.NS", "AIFL.NS", "AJRINFRA.NS", "ALCHEM.NS", "AMJUMBO.NS", "ANDHRACEMT.NS", "ANSALAPI.NS", "ARCOTECH.NS", "ARSSINFRA.NS", "ARTEDZ.NS", "ASIL.NS", "ATCOM.NS", "ATLASCYCLE.NS", "ATNINTER.NS", "AUTOLITIND.NS", "AUTORIDFIN.NS", "BANSAL.NS", "BGLOBAL.NS", "BHARATIDIL.NS", "BILENERGY.NS", "BIRLATYRE.NS", "BLUEBLENDS.NS", "BLUECHIP.NS", "BLUECOAST.NS", "BRFL.NS", "CANDC.NS", "CCCL.NS", "CELESTIAL.NS", "CKFSL.NS", "DFMFOODS.NS", "DIAPOWER.NS", "DOLPHINOFF.NS", "DQE.NS", "DSKULKARNI.NS", "EASTSUGIND.NS", "EASUNREYRL.NS", "EMCO.NS", "EON.NS", "EUROCERA.NS", "EUROMULTI.NS", "FEDDERELEC.NS", "FIVECORE.NS", "GAMMONIND.NS", "GANGOTRI.NS", "GBGLOBAL.NS", "GFSTEELS.NS", "GITANJALI.NS", "HINDNATGLS.NS", "ICSA.NS", "INDOSOLAR.NS", "IVRCLINFRA.NS", "JAINSTUDIO.NS", "JBFIND.NS", "JIKIND.NS", "JINDCOT.NS", "JMTAUTOLTD.NS", "JPINFRATEC.NS", "KEERTI.NS", "KGL.NS", "KSERASERA.NS", "KSK.NS", "LAKSHMIEFL.NS", "LEEL.NS", "MANPASAND.NS", "MBECL.NS", "MCDHOLDING.NS", "MERCATOR.NS", "METKORE.NS", "MODTHREAD.NS", "MOHOTAIND.NS", "MVL.NS", "NAKODA.NS", "NITINFIRE.NS", "NTL.NS", "NUTEK.NS", "OISL.NS", "OMKARCHEM.NS", "OPAL.NS", "OPTOCIRCUI.NS", "ORTEL.NS", "PDPL.NS", "PINCON.NS", "PRATIBHA.NS", "PRUDMOULI.NS", "PSL.NS", "PUNJLLOYD.NS", "QUINTEGRA.NS", "RADAAN.NS", "RAINBOWPAP.NS", "RAJVIR.NS", "RMMIL.NS", "RUSHABEAR.NS", "S&SPOWER.NS", "SATHAISPAT.NS", "SBIHOMEFIN.NS", "SHARONBIO.NS", "SHIRPUR-G.NS", "SICAL.NS", "SIIL.NS", "SKIL.NS", "SONISOYA.NS", "SPYL.NS", "SREINFRA.NS", "STAMPEDE.NS", "TALWALKARS.NS", "TALWGYM.NS", "TCIFINANCE.NS", "TECHNOFAB.NS", "THIRUSUGAR.NS", "TULSI.NS", "UNIPLY.NS", "UNITY.NS", "UNIVAFOODS.NS", "USK.NS", "VALECHAENG.NS", "VALUEIND.NS", "VICEROY.NS", "VIDEOIND.NS", "VIKASPROP.NS", "VISUINTL.NS", "VIVIMEDLAB.NS", "WINSOME.NS", "ZICOM.NS", "ACI.NS", "BALRAMCHIN.NS", "BBTC.NS"
         ]
                
    for stock in NSE_STOCKS:
        preprocess_stock(stock, "NSE_STOCKS")

# Define the schedule
schedule.every(0.1).minutes.do(run_nifty_50)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)




    
            
