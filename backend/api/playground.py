from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os

load_dotenv()


example = """
['S2eLeitlinie Diabetes in der Schwangerschaft 3 Auflage  DDG 2021 63 Empfehlungen Empfehlungsgrad 98 Jedes Entbindungszentrum soll ein interdisziplinaer erarbeitetes Be handlungsschema fuer die Diabetestherapie waehrend und unmittelbar nach der Geburt haben LoE 4 A 99 Zur Stoffwechselueberwachung waehrend der Geburt sollen einstuendli che GlukoseBlutglukosekontrollen erfolgen LoE 4 A 910 Waehrend der Entbindung sollten Zielwerte zwischen 90126 mgdl 5070 mmoll erreicht werden Groessere Stoffwechselschwankun gen ploetzliche Blutglukosespitzen oder hypoglykaemische Episoden sollten vermieden werden LoE 4 B 911 Nach der Entbindung sollte wegen des erhoehten Hypoglykaemierisikos in den ersten postpartalen Stunden die Insulintherapie individuell kurz fristig angepasst werden LoE 4 B', 'S2eLeitlinie Diabetes in der Schwangerschaft 3 Auflage  DDG 2021 14 Empfehlungen Empfehlungsgrad 23 Wegen der hohen Praevalenz einer Autoimmunthyreoiditis sollte praekonzeptionell bzw bei schwangeren Frauen mit Typ1Diabetes ein Screening auf TPOAntikoerper erfolgen LoE 1 B 24 Bei unbehandelten euthyreoten Schwangeren die TPOAKpositiv sind sollte die SerumTSHKonzentration alle 4 bis 8 Wochen ge messen werden LoE 2 bis 4 B 25 Bei Frauen mit TPOAntikoerperNachweis sollte bereits bei TSH  25 µUml auf Grund der moeglichen eingeschraenkten Schilddruesenhor monreserve die Therapie mit Levothyroxin begonnen werden LoE 1 bis 3 B 26 Bei Vorliegen einer latenten Hypothyreose soll umgehend eine Thera pie mit Levothyroxin eingeleitet werden LoE 1 A', 'S3Leitlinie Therapie des Typ1Diabetes 3 Auflage  Leitlinienreport  DDG 2021 4 1 Geltungsbereich und Zweck 11 Begruendung fuer die Auswahl des Leitlinienthemas Empfehlungen zur Betreuung der Schwangerschaft bei bekanntem Diabetes mellitus auf der Grundlage aktueller Daten Informationsbereitstellung fuer Schwangere als Ergaenzung der aerztlichen Beratung 12 Zielorientierung der Leitlinie Die Leitlinie hat zum Ziel alle relevanten Bereiche der Schwangerschaftsbetreuung zu bearbeiten 13 Zielpopulation z B Patientinnen Bevoelkerung Schwangere mit Typ1 oder Typ2Diabetes bei Planung einer Schwangerschaft oder bereits diagnos tizierter Schwangerschaft 14 Versorgungsbereich Ambulant und stationaer 15 AnwenderzielgruppeAdressatinnen Die Leitlinie richtet sich an Ärzte mit dem Schwerpunkt Diabetes Gynaekologen und Geburtshelfer Kin der und Jugendmediziner Perinatalmediziner Neonatologen und paediatrische Intensivmediziner Die Leitlinie dient zur Information fuer DiabetesberaterInnen sowie Patientinnen', 'S3Leitlinie Gestationsdiabetes mellitus GDM Diagnostik Therapie und Nachsorge 2 Auflage  DDG DGGGAGG 2018 6 1 Zielsetzung Ziel dieser Leitlinie ist die Verbesserung und Vereinheitlichung von Praevention Screening Diagnostik Therapie und Nachsorge bei Gestationsdiabetes durch evidenzbasierte Empfehlungen fuer den ambu lanten und stationaeren Bereich Adressaten der Leitlinie sind Fachaerzteinnen fuer Gynaekologie und Ge burtshilfe Innere Medizin und Allgemeinmedizin Diabetologeninnen Hebammen und Neonatolo geninnen Zudem dient die Leitlinie zur Information fuer an der Versorgung beteiligte Personengruppen wie z B Ernaehrungsberaterinnen Psychologinnen und andere mit der Gesundheit von Schwangeren befasste Gruppen Die Patientenzielgruppe sind Schwangere mit Gestationsdiabetes oder erhoehtem Risiko fuer Diabetes Die Leitlinie soll zudem die Bedeutung der Zusammenarbeit zwischen den Fachgebieten sowie den Betreuungsebenen hinweisen', 'EK Ib und fuehrt bei der Subgruppe von Frauen mit Diabetes zu fetaler Wachstumsretardierung Poston 2006 EK Ib Siehe auch AWMFLeitlinie zur Diagnostik und Therapie des hypertensiven Erkrankungen in der Schwangerschaft verwiesen Deutsche Gesellschaft fuer Gynaekologie und Geburtshilfe DGGG 2019 Empfehlungen Empfehlungsgrad 74 Doppleruntersuchungen bei Schwangeren mit Diabetes sollen ent sprechend den allgemeinen geburtshilflichen Indikationen erfolgen LoE 2 A']
"""
prompt_template = """
Summarize the following text according to these rules:
1. If the text bits are logically connected, summarize them cohesively; if they are not, summarize them individually.
2. If the text contains no logical or useful information, ignore it.
3. If no useful summary can be created, respond with "Not possible."
4. Start the summary immediately; avoid repeating instructions.
5. Use continuous text, not bullet points.

Text to summarize:
{example}
"""

formatted_prompt = prompt_template.format(example=example)


INFERENCE_TOKEN = os.getenv("INFERENCE_TOKEN")
MODEL_NAME = "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"
TEMPERATURE = 0.5

client = InferenceClient(token=INFERENCE_TOKEN)

response = client.text_generation(
    model=MODEL_NAME,
    prompt=formatted_prompt,
    temperature= TEMPERATURE,
    max_new_tokens= 1024,
    return_full_text= False,
)

print(response)
