#ifndef PDFGENERATOR_H
#define PDFGENERATOR_H

#include <QPdfWriter>
#include <QPainter>

class PDFGenerator
{
public:
    PDFGenerator(const QString& filename);
    void DrawHeader(const QString& text);
    void drawText(qreal x, qreal y, Qt::Alignment flags, const QString & text, int policeSize = 16);

private:
    QPdfWriter writer;
    QPainter painter;

    int dpm;
    int maxWidth;
    int maxHeight;
    int leftMargin;
};

#endif // PDFGENERATOR_H
