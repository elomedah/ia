"""Génère le PDF fictif 04_notes_de_frais.pdf du corpus (reportlab).
Le PDF contient volontairement un en-tête et un pied de page répétés,
pour illustrer le nettoyage nécessaire à l'ingestion (slide « Ingestion & Parsing »)."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

out = sys.argv[1] if len(sys.argv) > 1 else "04_notes_de_frais.pdf"
st = getSampleStyleSheet()
H1, H2, P = st["Title"], st["Heading2"], ParagraphStyle("p", parent=st["BodyText"], fontSize=10.5, leading=14)


def header_footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.drawString(40, A4[1] - 30, "Orbitale SAS - Direction Financière - Procédure FIN-PR-02 - Usage interne")
    c.drawString(40, 25, f"Document fictif à usage pédagogique (module FM02) - page {doc.page}")
    c.restoreState()


s = []
s += [Paragraph("Politique de remboursement des frais professionnels", H1),
      Paragraph("Version 2.1, applicable au 1er février 2026. Document fictif créé pour les besoins pédagogiques du module FM02.", P), Spacer(1, 10)]
s += [Paragraph("1. Principes", H2), Paragraph(
    "Les frais engagés pour le compte d'Orbitale sont remboursés sur justificatif, dans la limite des plafonds ci-dessous. "
    "Tout déplacement doit être autorisé au préalable par le manager. Les réservations de train, d'avion et d'hôtel se font en priorité "
    "via l'agence de voyage référencée, qui applique automatiquement la politique.", P)]
s += [Paragraph("2. Plafonds de remboursement", H2)]
data = [["Poste de dépense", "Plafond", "Commentaire"],
        ["Repas (midi ou soir)", "25 € par repas", "Hors invitation de clients"],
        ["Repas avec client", "60 € par personne", "Nom des invités obligatoire"],
        ["Hôtel à Paris", "150 € par nuit", "Petit-déjeuner inclus"],
        ["Hôtel en province", "110 € par nuit", "Petit-déjeuner inclus"],
        ["Hôtel à l'étranger", "180 € par nuit", "Selon la grille par pays"],
        ["Taxi ou VTC", "Sur justificatif", "Si pas de transport en commun après 21 h"]]
t = Table(data, colWidths=[150, 120, 210])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                       ("FONTSIZE", (0, 0), (-1, -1), 9.5)]))
s += [t, Spacer(1, 8)]
s += [Paragraph("3. Transports", H2), Paragraph(
    "Le train est le mode de transport privilégié, en seconde classe. La première classe est autorisée pour un trajet de plus de 3 heures. "
    "L'avion n'est autorisé que si le trajet en train dépasse 4 heures, en classe économique. "
    "L'utilisation du véhicule personnel est remboursée selon le barème kilométrique fiscal en vigueur, sur autorisation préalable.", P)]
s += [PageBreak()]
s += [Paragraph("4. Avance sur frais", H2), Paragraph(
    "Pour un déplacement dont le coût prévisionnel dépasse 500 euros, le collaborateur peut demander une avance sur frais "
    "au moins 10 jours avant le départ. L'avance est régularisée lors de la note de frais suivante.", P)]
s += [Paragraph("5. Déclaration et remboursement", H2), Paragraph(
    "Les notes de frais sont saisies dans MonEspace RH, rubrique « Frais », avec le formulaire FIN-03, accompagnées des justificatifs "
    "numérisés. Elles doivent être déclarées dans les 30 jours suivant la dépense ; au-delà de 90 jours, les frais ne sont plus remboursés. "
    "Le manager valide sous 5 jours ouvrés, puis le service comptable rembourse par virement sous 15 jours.", P)]
s += [Paragraph("6. Dépenses non remboursables", H2), Paragraph(
    "Ne sont pas remboursés : les amendes et contraventions, les dépenses de minibar, les frais de pressing pour un séjour de moins de 5 nuits, "
    "et les surclassements non autorisés.", P)]
s += [Paragraph("7. Contact", H2), Paragraph("Service comptabilité fournisseurs et frais : frais@orbitale.example", P)]
SimpleDocTemplate(out, pagesize=A4, topMargin=60, bottomMargin=50).build(s, onFirstPage=header_footer, onLaterPages=header_footer)
print("ok", out)
