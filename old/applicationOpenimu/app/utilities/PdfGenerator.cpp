#include "PdfGenerator.h"

PDFGenerator::PDFGenerator(const QString& filename):
    m_writer(filename),
    m_painter(&m_writer)
{
    QPageLayout pageLayout(QPageSize(QPageSize::A4),QPageLayout::Portrait,QMarginsF(15,15,15,15),QPageLayout::Millimeter, QMarginsF(15,15,15,15));
    m_writer.setPageLayout(pageLayout);

    m_painter.setPen(Qt::black);

    m_dpm = m_writer.resolution()/25.4;
    m_maxWidth = (210 - 30)*m_dpm;
    m_maxHeight = (297 - 30)*m_dpm;

    m_leftMargin = 7.5*72;
}

void PDFGenerator::DrawHeader(const QString& text)
{
    m_painter.fillRect(QRect(7.5*72, 15*m_dpm - 10 , m_maxWidth, 20),Qt::black);

    drawText(m_maxWidth/2, 30*m_dpm, Qt::AlignVCenter | Qt::AlignHCenter,text, 32);

    m_painter.fillRect(QRect(7.5*72,45*m_dpm-10,m_maxWidth,20),Qt::black);
}


void PDFGenerator::drawText(qreal x, qreal y, Qt::Alignment flags,
                            const QString & text, int policeSize)
{
    QFont pFont = m_painter.font();
    int pSize = pFont.pointSize();
    pFont.setPointSize(policeSize);
    m_painter.setFont(pFont);

    const qreal size = 32767.0;
    QPointF corner(x + m_leftMargin, y - size);
    if (flags & Qt::AlignHCenter) corner.rx() -= size/2.0;
    else if (flags & Qt::AlignRight) corner.rx() -= size;
    if (flags & Qt::AlignVCenter) corner.ry() += size/2.0;
    else if (flags & Qt::AlignTop) corner.ry() += size;
    else flags |= Qt::AlignBottom;
    QRectF rect(corner, QSizeF(size, size));
    m_painter.drawText(rect, flags, text);

    pFont.setPointSize(pSize);
    m_painter.setFont(pFont);
}
