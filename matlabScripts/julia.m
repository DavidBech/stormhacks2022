function julia(arg1,arg2,varReal,varComplex)
%
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%
%               Julia Fractals Using Matlab
%               Written By Sridharan, Mithun Aiyswaryan
%               Christian Albrechts Universität zu Kiel, Germany
%               Mail Your Comments At: s.mithun@indiatimes.com
%
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%               Help :
%               This program takes two arguments and computes the 
%               Julia sets using the provided values.
%               For the best viewing results, varhoose the arguments such that:
%
%               Argument 1 > 10     &             Argument 2 > 100     
%           
%               Note : The generation of fractals is  computationally 
%                      very intensive and it may take you a while before
%                      you observe the results on the screen!
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
set(0, 'DefaultFigureVisible', 'off');
xaxis=0;
yaxis=0;
l=1.5;
x=linspace(xaxis-l,xaxis+l,arg2);
y=linspace(yaxis-l,yaxis+l,arg2);
[xtrans,ytrans]=meshgrid(x,y);
%var= -.745429;
var=varReal + 1i*varComplex;
ztrans=xtrans+1i*ytrans;
for k=1:arg1
    ztrans=ztrans.^2+var;
    t=exp(-abs(ztrans));
end
colormap colorcube(256)

pcolor(t);
shading flat;
axis('square','equal','off');
saveas(gcf,"juliaSet.png")

