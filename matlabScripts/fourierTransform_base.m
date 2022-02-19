function [X] =fourierTransform_base (x)
    syms t;
    x = sin(t);
    X = fourier(x);
end
