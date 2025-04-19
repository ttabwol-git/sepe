"use client";

import { removeSubscription } from "@/api/subscription";
import { Button } from "@/components/button";
import { Fieldset } from "@/components/fieldset";
import { Strong, Text } from "@/components/text";
import { ArrowLeftCircleIcon, TrashIcon } from "@heroicons/react/20/solid";
import clsx from "clsx";

export default function Step3({
  setCurrentStep,
  subscriptionToken,
  setSubscriptionToken,
}: {
  setCurrentStep: (step: number) => void;
  subscriptionToken: string;
  setSubscriptionToken: (token: string) => void;
}) {
  const handleUnsubscribe = () => {
    if (!subscriptionToken) return;

    removeSubscription(subscriptionToken)
      .then(() => setSubscriptionToken("")) // Clear the token after unsubscription
      .catch((error) => {
        // Handle any errors that occur during unsubscription
        console.error("Unsubscription error:", error);
      });
  };
  const handleGoBack = () => {
    setCurrentStep(1); // Go back to the first step
  };
  return (
    <Fieldset className="w-96 space-y-6">
      <Text>
        <Strong>Alright, you&apos;re now subscribed!</Strong> — Check the
        backend console.
      </Text>
      <Text>
        The engine will run in the background to check the availability of SEPE
        offices for the submitted postal code. If any office is available,{" "}
        <Strong>the results will be printed in the console</Strong>. Note that
        this process runs only
        <Strong> once per postal code</Strong>.
      </Text>
      <Text>
        If a new subscription is submitted for the same postal code, the backend
        will append the new subscriber to the existing process and extend its
        expiration time accordingly. If a new subscriber is added using a
        different postal code, a new process will be created.
      </Text>
      <Text>
        <Strong>The subscription lasts for 24 hours</Strong>, but you can always
        manually unsubscribe using the same token with a button like the one
        below.
      </Text>
      <Button
        color={"red"}
        disabled={!subscriptionToken}
        onClick={handleUnsubscribe}
        className={clsx("w-96", {
          "cursor-not-allowed opacity-50": !subscriptionToken,
          "cursor-pointer": subscriptionToken,
        })}
      >
        <TrashIcon />
        Unsubscribe
      </Button>
      <Text>
        If you want to resubscribe, just go back to the first step and submit a
        new subscription.
      </Text>
      <Button outline className="hover:cursor-pointer" onClick={handleGoBack}>
        <ArrowLeftCircleIcon />
        Go Back
      </Button>
    </Fieldset>
  );
}
