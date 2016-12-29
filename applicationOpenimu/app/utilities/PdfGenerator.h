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
    QPdfWriter m_writer;
    QPainter m_painter;

    int m_dpm;
    int m_maxWidth;
    int m_maxHeight;
    int m_leftMargin;
};

#endif // PDFGENERATOR_H
