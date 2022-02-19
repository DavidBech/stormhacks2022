function fourierTransform_base ()
    set(0, 'DefaultFigureVisible', 'off');
    SampleTime = 1/50;
    SampleFreq = 1/SampleTime;
    t = 0:SampleTime:10-SampleTime;
    x = cos(2*pi*t);
    X = fft(x);
    n = length(x);
    %f = (0:length(X)-1)*SampleFreq/length(X);
    fshift = (-n/2:n/2-1)*(SampleFreq/n);
    Xshift = fftshift(X);
    plot(fshift, abs(Xshift), "LineWidth", 2)
    axis([-5, 5, -1, 300])
    xlabel("Frequency (Hz)")
    ylabel("Magnitude")
    saveas(gcf,"test.jpg")
    %plot(f, abs(X))
end
