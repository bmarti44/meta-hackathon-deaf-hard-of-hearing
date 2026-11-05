# Provisional descriptive finding: Gen 19 in simulated reverberant rooms

> Reported 2026-11-04 ~21:58 at Astra's recommendation
> ([astra-prelaunch-review.md](./astra-prelaunch-review.md)). It uses her
> wording. It is **provisional**: it will be recomputed after the
> direct-arrival correction, and both versions will be kept.

> On the Gen27 reverberant development panel, Gen19 seed 17 increased mean SI-SDR relative to unprocessed mixtures at −5 dB by +0.37 dB with synthetic RIRs and +0.73 dB with measured RIRs, while mean STOI decreased by 0.029 and 0.017. For reverberant target-only speech, mean changes were −1.65 dB SI-SDR and −0.064 STOI. These results use the current peak-anchored early reference and fixed model-delay alignment.

This is **metric degradation on simulated reverberant speech**. It is not
established intelligibility loss or harm to cochlear-implant listeners,
and convolving speech with measured RIRs still produces simulated
material.

For comparison, on the dry 16-voice screen-v2 panel the same model gains
+2.385 dB at −5 dB.

This is why Gen 27 (room augmentation) is the next experiment.
