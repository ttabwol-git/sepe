"use client";

import { Divider } from "@/components/divider";
import classNames from "classnames";
import Image from "next/image";
import { useState } from "react";
import Step1 from "./step1";
import Step2 from "./step2";
import Step3 from "./step3";

const classes = {
  parentContainer: classNames(
    "relative",
    "isolate",
    "flex",
    "min-h-screen",
    "pt-20"
  ),
  childContainer: classNames("flex-1"),
  logoContainer: classNames(
    "flex",
    "justify-center",
    "items-center",
    "space-x-4",
    "pb-4",
    "text-indigo-300",
    "font-mono",
    "text-4xl"
  ),
  logo: classNames("logoIndigoTint"),
  title: classNames("text-xl", "text-center", "p-5"),
};

export default function Home() {
  const [currentStep, setCurrentStep] = useState(1);
  const [subscriptionToken, setSubscriptionToken] = useState("");

  return (
    <div className={classes.parentContainer}>
      <div className={classes.childContainer}>
        <div className={classes.logoContainer}>
          <Image
            src="/logo.svg"
            alt="Logo"
            width={50}
            height={50}
            className={classes.logo}
            priority={true}
          />
          <div>SepeCheck</div>
        </div>
        <Divider className="mt-8" />
        <div className="flex justify-center pt-8">
          {currentStep === 1 && (
            <Step1
              setCurrentStep={setCurrentStep}
              setSubscriptionToken={setSubscriptionToken}
            />
          )}
          {currentStep === 2 && (
            <Step2
              setCurrentStep={setCurrentStep}
              subscriptionToken={subscriptionToken}
            />
          )}
          {currentStep === 3 && (
            <Step3
              setCurrentStep={setCurrentStep}
              subscriptionToken={subscriptionToken}
              setSubscriptionToken={setSubscriptionToken}
            />
          )}
        </div>
      </div>
    </div>
  );
}
