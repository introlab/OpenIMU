#include "PdfGenerator.h"

PDFGenerator::PDFGenerator(const QString& filename):
writer(filename),
painter(&writer)
{
    QPageLayout pageLayout(QPageSize(QPageSize::A4),QPageLayout::Portrait,QMarginsF(15,15,15,15),QPageLayout::Millimeter, QMarginsF(15,15,15,15));
    writer.setPageLayout(pageLayout);

    painter.setPen(Qt::black);

    dpm = writer.resolution()/25.4;
    maxWidth = (210 - 30)*dpm;
    maxHeight = (297 - 30)*dpm;

    leftMargin = 7.5*72;
}

void PDFGenerator::DrawHeader(const QString& text)
{
    painter.fillRect(QRect(7.5*72, 15*dpm - 10 , maxWidth, 20),Qt::black);

    drawText(maxWidth/2, 30*dpm, Qt::AlignVCenter | Qt::AlignHCenter,text, 32);

    painter.fillRect(QRect(7.5*72,45*dpm-10,maxWidth,20),Qt::black);
}


void PDFGenerator::drawText(qreal x, qreal y, Qt::Alignment flags,
              const QString & text, int policeSize)
{

    QFont pFont = painter.font();
    int pSize = pFont.pointSize();
    pFont.setPointSize(policeSize);
    painter.setFont(pFont);

   const qreal size = 32767.0;
   QPointF corner(x + leftMargin, y - size);
   if (flags & Qt::AlignHCenter) corner.rx() -= size/2.0;
   else if (flags & Qt::AlignRight) corner.rx() -= size;
   if (flags & Qt::AlignVCenter) corner.ry() += size/2.0;
   else if (flags & Qt::AlignTop) corner.ry() += size;
   else flags |= Qt::AlignBottom;
   QRectF rect(corner, QSizeF(size, size));
   painter.drawText(rect, flags, text);

   pFont.setPointSize(pSize);
   painter.setFont(pFont);
}
